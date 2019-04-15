from django.test import TestCase
from rest_framework.test import APIRequestFactory
from movies.models import Movie, Comment
from movies.views import CommentsList, CommentsForMovie


class MovieListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        Movie.objects.create(title="test_movie_1")
        Movie.objects.create(title="test_movie_2")

        movie1 = Movie.objects.get(title="test_movie_1")
        movie2 = Movie.objects.get(title="test_movie_2")

        Comment.objects.create(body="lorem ipsum 1", movie_id=movie1)
        Comment.objects.create(body="lorem ipsum 2", movie_id=movie2)
        Comment.objects.create(body="lorem ipsum 2", movie_id=movie2)

    def test_structure(self):
        """
        Test structure of response JSON.
        """
        request = self.factory.get('api/comments/')

        response = CommentsList.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertAlmostEqual(len(response.data), 3)

        for c in response.data:
            self.assertIsInstance(c, dict)

    def test_single_comment(self):
        request = self.factory.get('api/comments/')

        response = CommentsList.as_view()(request)

        self.assertEqual(response.data[0].get('body'), "lorem ipsum 1")
        self.assertEqual(response.data[0].get('movie_id'), 1)
        self.assertEqual(response.data[0].get('id'), 1)

    def test_comment_creation(self):
        test_data = {
            "body": "Very interesting comment",
            "movie_id": 1
        }

        request = self.factory.post('api/comments/', test_data)
        response = CommentsList.as_view()(request)

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)

        for k, v in test_data.items():
            self.assertEqual(response.data.get(k), v)

    def test_comments_for_movie1(self):
        request = self.factory.get('api/comments/1/')
        response = CommentsForMovie.as_view()(request, pk=1)
        self.assertEqual(len(response.data), 1)

    def test_comments_for_movie2(self):
        request = self.factory.get('api/comments/2/')
        response = CommentsForMovie.as_view()(request, pk=2)
        self.assertEqual(len(response.data), 2)

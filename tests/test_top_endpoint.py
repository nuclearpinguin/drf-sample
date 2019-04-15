from django.test import TestCase
from rest_framework.test import APIRequestFactory
from movies.models import Movie, Comment
from movies.views import TopList


class MovieListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        Movie.objects.create(title="test_movie_1")
        Movie.objects.create(title="test_movie_2")
        Movie.objects.create(title="test_movie_3")

        movie1 = Movie.objects.get(title="test_movie_1")
        movie2 = Movie.objects.get(title="test_movie_2")
        movie3 = Movie.objects.get(title="test_movie_3")

        for i in range(15):
            Comment.objects.create(body=f"lorem ipsum {i}", movie_id=movie1)

        for i in range(5):
            Comment.objects.create(body=f"lorem ipsum {i}", movie_id=movie2)
            Comment.objects.create(body=f"lorem ipsum {i}", movie_id=movie3)

    def test_structure(self):
        request = self.factory.get('api/top/')

        response = TopList.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertAlmostEqual(len(response.data), 3)

        for c in response.data:
            self.assertIsInstance(c, dict)

    def test_ranking(self):
        request = self.factory.get('api/top/')
        response = TopList.as_view()(request)

        ranking = response.data
        movie1 = ranking[0]
        movie2 = ranking[1]
        movie3 = ranking[2]

        self.assertEqual(movie1['rank'], 1)
        self.assertEqual(movie2['rank'], 2)

        # Does movies with the same amount of comment has the same rank?
        self.assertEqual(movie2['rank'], movie3['rank'])

        self.assertEqual(movie1['total_comment'], 15)
        self.assertEqual(movie2['total_comment'], 5)
        self.assertEqual(movie3['total_comment'], 5)

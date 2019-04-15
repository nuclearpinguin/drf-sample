from django.test import TestCase
from movies.models import Movie, Comment


class MovieTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(title="test_movie_1",
                             genre="awesome",
                             director="best")

    def test_movie_creation(self):
        test = Movie.objects.get(title="test_movie_1")

        self.assertEqual(test.title, 'test_movie_1')
        self.assertEqual(test.genre, 'awesome')
        self.assertEqual(test.director, 'best')
        self.assertEqual(test.metascore, None)


class CommentTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(title="test_movie_2")
        movie = Movie.objects.get(title="test_movie_2")

        Comment.objects.create(body="lorem ipsum",
                               movie_id=movie)

    def test_comment_creation(self):
        test = Comment.objects.get(body="lorem ipsum")
        self.assertEqual(test.body, 'lorem ipsum')

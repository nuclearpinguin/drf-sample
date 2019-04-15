from django.test import TestCase
from rest_framework.test import APIRequestFactory
from movies.models import Movie
from movies.views import MoviesList


class MovieListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        Movie.objects.create(title="test_movie_1",
                             genre="awesome",
                             director="best")

        Movie.objects.create(title="test_movie_2",
                             genre="awesome2")

    def test_structure(self):
        request = self.factory.get('api/movies/')

        response = MoviesList.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertAlmostEqual(len(response.data), 2)
        self.assertIsInstance(response.data[0], dict)
        self.assertIsInstance(response.data[1], dict)

    def test_single_movie(self):
        request = self.factory.get('api/movies/')

        response = MoviesList.as_view()(request)

        self.assertEqual(response.data[0].get('title'), "test_movie_1")
        self.assertEqual(response.data[0].get('genre'), "awesome")
        self.assertEqual(response.data[0].get('director'), "best")

    def test_movie_creation(self):
        """
        Test if data is fetched from OMDb and returned in
        enriched response.
        """
        test_data = {
            "title": "Lord of the Rings",
            "director": "Peter Jackson",
            "genre": "Adventure, Drama, Fantasy",
            "metascore": 92
        }

        request = self.factory.post('api/movies/', {'title': test_data['title']})
        response = MoviesList.as_view()(request)

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)

        for k, v in test_data.items():
            self.assertEqual(response.data.get(k), v)

    def test_metascore_filter(self):
        """
        Test if metascore param works
        """
        test_data = {
            "title": "Lord of the Rings",
            "director": "Peter Jackson",
            "genre": "Adventure, Drama, Fantasy",
            "metascore": 92
        }
        Movie.objects.create(**test_data)

        request = self.factory.get('api/movies?metascore=80')
        response = MoviesList.as_view()(request)
        self.assertEqual(len(response.data), 1)

        request = self.factory.get('api/movies?metascore=95')
        response = MoviesList.as_view()(request)
        self.assertEqual(len(response.data), 0)

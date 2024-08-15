import unittest
from unittest.mock import patch
from movie_app.movie_app import MovieApp
from storage.istorage import IStorage

class MockStorage(IStorage):
    def __init__(self):
        self.movies = {}

    def list_movies(self):
        return self.movies

    def add_movie(self, title, year, rating, poster):
        self.movies[title] = {"year": year, "rating": rating, "poster": poster}

    def delete_movie(self, title):
        if title in self.movies:
            del self.movies[title]

    def update_movie(self, title, rating):
        if title in self.movies:
            self.movies[title]['rating'] = rating

class TestMovieApp(unittest.TestCase):
    def setUp(self):
        self.storage = MockStorage()
        self.app = MovieApp(self.storage)

    @patch('movie_app.movie_app.requests.get')
    def test_add_movie(self, mock_get):
        mock_get.return_value.json.return_value = {
            "Response": "True",
            "Year": "2010",
            "imdbRating": "8.8",
            "Poster": "http://example.com/poster.jpg"
        }
        self.app._command_add_movie()
        self.assertIn("Inception", self.storage.list_movies())

    def test_delete_movie(self):
        self.storage.add_movie("Inception", 2010, 8.8, "http://example.com/poster.jpg")
        self.app._command_delete_movie()
        self.assertNotIn("Inception", self.storage.list_movies())

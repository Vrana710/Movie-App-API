import pytest
from unittest.mock import patch
from movie_app.movie_app import MovieApp
from storage.istorage import IStorage

# Mock storage implementation
class MockStorage(IStorage):
    def __init__(self):
        self.movies = {}

    def list_movies(self):
        return self.movies

    def add_movie(self, title, year, rating, poster, language, country, awards, imdbID):
        self.movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster,
            "language": language,
            "country": country,
            "awards": awards,
            "imdbID": imdbID
        }

    def delete_movie(self, title):
        if title in self.movies:
            del self.movies[title]

    def update_movie(self, title, rating=None, **kwargs):
        if title in self.movies:
            if rating is not None:
                self.movies[title]['rating'] = rating
            for key, value in kwargs.items():
                if key in self.movies[title]:
                    self.movies[title][key] = value

    def check_if_exists(self, title):
        return title in self.movies

# Pytest fixture for setup
@pytest.fixture
def app():
    storage = MockStorage()
    app = MovieApp(storage)
    return app, storage

# Test adding a movie with mocked fetch method
@patch.object(MovieApp, '_fetch_movie_data', return_value={
    "Title": "Inception",
    "Year": "2010",
    "imdbRating": "8.8",
    "Poster": "http://example.com/poster.jpg",
    "Language": "English",
    "Country": "USA",
    "Awards": "Nominated for 8 Oscars.",
    "imdbID": "tt1375666"
})
@patch('builtins.input', side_effect=['Inception'])
def test_add_movie(mock_input, mock_fetch, app):
    app, storage = app

    app._command_add_movie()

    # Validate the movie is added correctly
    movie = storage.list_movies().get("Inception")
    assert movie is not None
    assert movie["year"] == "2010"
    assert movie["rating"] == "8.8"
    assert movie["poster"] == "http://example.com/poster.jpg"
    assert movie["language"] == "English"
    assert movie["country"] == "USA"
    assert movie["awards"] == "Nominated for 8 Oscars."
    assert movie["imdbID"] == "tt1375666"

# Test deleting a movie
@patch('builtins.input', side_effect=['The Lord of the Rings: The Fellowship of the Ring'])
def test_delete_movie(mock_input, app):
    app, storage = app
    storage.add_movie(
        "The Lord of the Rings: The Fellowship of the Ring",
        2001,
        8.9,
        "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_SX300.jpg",
        "English, Sindarin",
        "New Zealand, United States",
        "Won 4 Oscars. 125 wins & 127 nominations total",
        "tt0120737"
    )
    app._command_delete_movie()
    assert "The Lord of the Rings: The Fellowship of the Ring" not in storage.list_movies()

import unittest
import os
from storage.storage_json import StorageJson

class TestStorageJson(unittest.TestCase):
    def setUp(self):
        self.file_path = 'test_movies.json'
        self.storage = StorageJson(self.file_path)

    def tearDown(self):
        # Ensure the test file is removed after each test
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_add_movie(self):
        self.storage.add_movie(
            "Inception", 
            2010, 
            8.8, 
            "http://example.com/poster.jpg",
            language="English",
            country="USA",
            awards="Nominated for 8 Oscars.",
            imdbID="tt1375666"
        )
        movies = self.storage.list_movies()
        self.assertIn("Inception", movies)
        self.assertEqual(movies["Inception"]["year"], 2010)
        self.assertEqual(movies["Inception"]["rating"], 8.8)
        self.assertEqual(movies["Inception"]["language"], "English")
        self.assertEqual(movies["Inception"]["country"], "USA")
        self.assertEqual(movies["Inception"]["awards"], "Nominated for 8 Oscars.")
        self.assertEqual(movies["Inception"]["imdbID"], "tt1375666")

    def test_delete_movie(self):
        self.storage.add_movie(
            "Inception", 
            2010, 
            8.8, 
            "http://example.com/poster.jpg",
            language="English",
            country="USA",
            awards="Nominated for 8 Oscars.",
            imdbID="tt1375666"
        )
        self.storage.delete_movie("Inception")
        movies = self.storage.list_movies()
        self.assertNotIn("Inception", movies)

    def test_update_movie(self):
        self.storage.add_movie(
            "Inception", 
            2010, 
            8.8, 
            "http://example.com/poster.jpg",
            language="English",
            country="USA",
            awards="Nominated for 8 Oscars.",
            imdbID="tt1375666"
        )
        self.storage.update_movie(
            "Inception", 
            rating=9.0
        )
        movies = self.storage.list_movies()
        self.assertEqual(movies["Inception"]["rating"], 9.0)

if __name__ == '__main__':
    unittest.main()

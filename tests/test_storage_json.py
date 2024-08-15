import unittest
import os
from storage.storage_json import StorageJson

class TestStorageJson(unittest.TestCase):
    def setUp(self):
        self.file_path = 'test_movies.json'
        self.storage = StorageJson(self.file_path)

    def tearDown(self):
        os.remove(self.file_path)

    def test_add_movie(self):
        self.storage.add_movie("Inception", 2010, 8.8, "http://example.com/poster.jpg")
        movies = self.storage.list_movies()
        self.assertIn("Inception", movies)
        self.assertEqual(movies["Inception"]["year"], 2010)

    def test_delete_movie(self):
        self.storage.add_movie("Inception", 2010, 8.8, "http://example.com/poster.jpg")
        self.storage.delete_movie("Inception")
        movies = self.storage.list_movies()
        self.assertNotIn("Inception", movies)

    def test_update_movie(self):
        self.storage.add_movie("Inception", 2010, 8.8, "http://example.com/poster.jpg")
        self.storage.update_movie("Inception", 9.0)
        movies = self.storage.list_movies()
        self.assertEqual(movies["Inception"]["rating"], 9.0)

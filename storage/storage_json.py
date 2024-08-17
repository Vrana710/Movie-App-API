import json
import os
from storage.istorage import IStorage

class StorageJson(IStorage):
    def __init__(self, file_path):
        """
        Initializes a new instance of StorageJson class.

        :param file_path: A string representing the path to the JSON file where the movie data will be stored.
        """
        self.file_path = file_path
        
    
    def check_if_exists(self, title):
        """
        Checks if the Movie name exists in the database.

        :param title: Title of the movie to check.
        :return: True if the movie exists, False otherwise.
        """
        data = self._load_data()
        return title in data

    
    def _load_data(self):
        """
        Loads data from the JSON file specified by the file_path attribute.

        This method attempts to open the JSON file at the specified path 
        and load its contents into a Python dictionary.
        If the file does not exist or cannot be opened, an empty dictionary is returned.

        Parameters:
        self (StorageJson): The instance of the StorageJson class.

        Returns:
        dict: A dictionary containing the loaded movie data. 
        If the file does not exist or cannot be opened, an empty dictionary is returned.
        """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}
            return data

    
    def _save_data(self, data):
        """
        Saves the provided movie data to the JSON file specified by the file_path attribute.

        This method attempts to open the JSON file at the specified path 
        and write the provided movie data 
        into it in a formatted manner. If the file does not exist, it will be created.

        Parameters:
        self (StorageJson): The instance of the StorageJson class.
        data (dict): A dictionary containing the movie data to be saved. 
        The keys of the dictionary are the movie titles,
        and the values are dictionaries containing 
        the movie details (year, rating, poster).

        Returns:
        None
        """
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    
    def list_movies(self):
        """
        Retrieves a list of all movies stored in the JSON file.

        This method calls the private method '_load_data' to load the movie data 
        from the JSON file specified by the 'file_path' attribute.
        It then returns the loaded data as a dictionary.

        Parameters:
        self (StorageJson): The instance of the StorageJson class.

        Returns:
        dict: A dictionary containing the loaded movie data. 
        The keys of the dictionary are the movie titles,
        and the values are dictionaries containing 
        the movie details (year, rating, poster).
        """
        return self._load_data()

    
    def add_movie(self, title, year, rating, poster, language,  country, awards, imdbID, note=None):
        """
        Adds a new movie to the storage.

        This method takes in the title, year, rating, and poster of a movie,
        and adds them to the storage. The movie data is stored in a dictionary,
        where the movie title is the key and the movie details (year, rating, poster)
        are stored as a nested dictionary.

        Parameters:
        self (StorageJson): The instance of the StorageJson class.
        title (str): The title of the movie to be added.
        year (int): The release year of the movie.
        rating (float): The rating of the movie.
        poster (str): The URL of the movie poster.

        Returns:
        None
        """
        data = self._load_data()
        data[title] = {
            "year": year, 
            "rating": rating, 
            "poster": poster, 
            "language" : language, 
            "country": country, 
            "awards": awards,
            "imdbID": imdbID,  # Optional, default is empty string if not provided in CSV file
            "note": note
        }
        self._save_data(data)

    
    def delete_movie(self, title):
        """
        Deletes a movie from the storage based on the provided title.

        This method retrieves the current movie data from the JSON file using 
        the '_load_data' method.
        It then checks if a movie with the given title exists in the data.
        If the movie exists, it removes the movie from the data and saves 
        the updated data back to the JSON file using the '_save_data' method.

        Parameters:
        self (StorageJson): The instance of the StorageJson class.
        title (str): The title of the movie to be deleted.

        Returns:
        None
        """
        data = self._load_data()
        if title in data:
            del data[title]
            self._save_data(data)

    
    def update_movie(self, title, year=None, rating=None, language=None,  country=None, awards=None, note=None):
        """
        Updates the year and rating of a movie in the storage based on the provided title. 

        This method retrieves the current movie data from the JSON file using 
        the '_load_data' method.
        It then checks if a movie with the given title exists in the data.
        If the movie exists, it updates the year and rating of the movie in the data 
        and saves the updated data back to the JSON file using the '_save_data' method.

        Parameters:
        self (StorageJson): The instance of the StorageJson class.
        title (str): The title of the movie to be updated.
        year (int): The new release year of the movie.
        rating (float): The new rating of the movie.

        Returns:
        None
        """
        data = self._load_data()
        if title in data:
            if year is not None:
                data[title]["year"] = year
            if rating is not None:
                data[title]['rating'] = rating
            if language is not None:
                 data[title]["language"] = language
            if country is not None:
                data[title]['country'] = country
            if awards is not None:
                data[title]['awards'] = awards
            if note is not None:
                data[title]['note'] = note
            self._save_data(data)
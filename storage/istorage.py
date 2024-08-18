from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def check_if_exists(self, title):
        """
        Method to check if Movie exists in database
        """
        raise NotImplementedError

    @abstractmethod
    def list_movies(self):
        """Returns a dictionary of movies."""
        pass
        raise NotImplementedError

    @abstractmethod
    def add_movie(self, 
                  title, 
                  year, 
                  rating, 
                  poster, 
                  language, 
                  country, 
                  awards, 
                  imdbID, note=None):
        """
        Adds a movie to the storage.

        Parameters:
        title (str): The title of the movie.
        year (int): The release year of the movie.
        rating (float): The rating of the movie.
        poster (str): The URL of the movie poster.
        language (str): The language of the movie.
        country (str): The country where the movie was produced.
        awards (str): The awards received by the movie.
        imdbID (str): The unique identifier for the movie on IMDb.
        note (str, optional): Additional notes about the movie. Defaults to None.

        Returns:
        None
        """
        pass
        raise NotImplementedError

    @abstractmethod
    def delete_movie(self, title):
        """Deletes a movie from the storage."""
        pass
        raise NotImplementedError

    @abstractmethod
    def update_movie(self, 
                     title, 
                     year=None, 
                     rating=None, 
                     language=None, 
                     country=None, 
                     awards=None, 
                     note=None):
        """
        Updates a movie's information in the storage.

        Parameters:
        title (str): The title of the movie to be updated.
        year (int, optional): The new release year of the movie. Defaults to None.
        rating (float, optional): The new rating of the movie. Defaults to None.
        language (str, optional): The new language of the movie. Defaults to None.
        country (str, optional): The new country where the movie was produced. Defaults to None.
        awards (str, optional): The new awards received by the movie. Defaults to None.
        note (str, optional): The new additional notes about the movie. Defaults to None.

        Returns:
        None
        """
        pass
        raise NotImplementedError

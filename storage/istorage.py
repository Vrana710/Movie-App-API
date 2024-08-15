from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def check_if_exists(self, title):
        """
        Method to check if Movie exists in database
        """

    @abstractmethod
    def list_movies(self):
        """Returns a dictionary of movies."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Adds a movie to the storage."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Deletes a movie from the storage."""
        pass

    @abstractmethod
    def update_movie(self, title, year, rating):
        """Updates a movie's rating."""
        pass

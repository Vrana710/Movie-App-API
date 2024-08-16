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
    def add_movie(self, title, year, rating, poster, language, country, awards, note=None):
        """Adds a movie to the storage."""
        pass
        raise NotImplementedError

    @abstractmethod
    def delete_movie(self, title):
        """Deletes a movie from the storage."""
        pass
        raise NotImplementedError

    @abstractmethod
    def update_movie(self, title, year=None, rating=None, language=None, country=None, awards=None , note=None):
        """Updates a movie's rating."""
        pass
        raise NotImplementedError

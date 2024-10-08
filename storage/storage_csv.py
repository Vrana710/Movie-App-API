import csv
from storage.istorage import IStorage

class StorageCsv(IStorage):
    def __init__(self, file_path):
        """
        Initializes a new instance of StorageCsv class.

        :param file_path: A string representing the path to the CSV file where movie data will be stored.
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
        Loads movie data from the CSV file into a dictionary.

        Parameters:
        - self: The instance of the StorageCsv class.

        Returns:
        - movies: A dictionary containing movie titles as keys and 
        their respective information (year, rating, poster) as values.

        Raises:
        - FileNotFoundError: If the specified file path does not exist.
        - csv.Error: If there is an error reading the CSV file.
        """
        movies = {}
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not row['title']:  # Skip any empty rows
                        continue
                    try:
                        title = row['title']
                        movies[title] = {
                            'year': int(row['year']),
                            'rating': float(row['rating']),
                            'poster': row['poster'],
                            'language' : row['language'], 
                            'country' : row['country'], 
                            'awards' : row['awards'],
                            'imdbID' : row['imdbID'],
                            'note': row['note'] if row['note'] else None,  # Convert empty string to None for consistency with other values
                        }
                    except KeyError as e:
                        print(f"\nMissing expected column in row: {row}. Error: {e}")
                    except ValueError as e:
                        print(f"\nError converting data types in row: {row}. Error: {e}")
        except FileNotFoundError:
            print(f"\nError: The file {self.file_path} was not found.")
        except csv.Error as e:
            print(f"\nError reading CSV file {self.file_path}: {e}")

        return movies

    
    def _save_data(self, data):
        """
        Saves movie data to the CSV file.

        Parameters:
        - self (StorageCsv): The instance of the StorageCsv class.
        - data (dict): A dictionary containing movie titles as keys 
        and their respective information (year, rating, poster) as values.

        Returns:
        None

        Raises:
        - csv.Error: If there is an error saving data to the CSV file. ,
        """
        try:
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['title', 
                              'year', 
                              'rating', 
                              'poster', 
                              'language',  
                              'country', 
                              'awards', 
                              'imdbID',
                              'note']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for title, info in data.items():
                    writer.writerow({
                        'title': title,
                        'year': info['year'],
                        'rating': info['rating'],
                        'poster': info['poster'],
                        'language' : info['language'], 
                        'country' : info['country'], 
                        'awards' : info['awards'],
                        'imdbID' : info['imdbID'],  # Optional, default is empty string if not provided in CSV file
                        'note' :'' #Optional
                    })
        except csv.Error as e:
            print(f"\nError saving data to {self.file_path}: {e}")

    
    def list_movies(self):
        """
        Retrieves a list of all movies stored in the CSV file.

        This method reads the CSV file specified by the 
        file_path attribute and returns a dictionary
        containing movie titles as keys and their respective information 
        (year, rating, poster) as values.

        Parameters:
        - self (StorageCsv): The instance of the StorageCsv class.

        Returns:
        - dict: A dictionary containing movie titles as keys and 
        their respective information (year, rating, poster) as values.
        """
        return self._load_data()

    
    def add_movie(self, 
                  title, 
                  year, 
                  rating, 
                  poster, 
                  language, 
                  country, 
                  awards, 
                  imdbID, 
                  note=None):
        """
        Adds a new movie to the CSV file.

        This method reads the existing movie data from the CSV file, 
        adds a new movie with the given title, year, rating, poster, language, 
        country, awards, imdbID, and note (optional), and then saves the updated 
        data back to the CSV file.

        Parameters:
        - self (StorageCsv): The instance of the StorageCsv class.
        - title (str): The title of the movie to be added.
        - year (int): The release year of the movie.
        - rating (float): The rating of the movie.
        - poster (str): The URL of the movie poster.
        - language (str): The language of the movie.
        - country (str): The country where the movie was produced.
        - awards (str): The awards received by the movie.
        - imdbID (str): The unique identifier for the movie on IMDb.
        - note (str, optional): Additional notes about the movie. Defaults to None.


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
            "note": note # Optional, default is empty string if not provided in CSV file
            } 
        self._save_data(data)

    
    def delete_movie(self, title):
        """
        Deletes a movie from the CSV file based on the given title.

        This method reads the existing movie data from the CSV file,
        checks if a movie with the given title exists, deletes it if found,
        and then saves the updated data back to the CSV file.

        Parameters:
        - self (StorageCsv): The instance of the StorageCsv class.
        - title (str): The title of the movie to be deleted.

        Returns:
        None
        """
        data = self._load_data()
        if title in data:
            del data[title]
            self._save_data(data)
            

    def update_movie(self, 
                     title, 
                     year=None, 
                     rating=None,  
                     language=None, 
                     country=None, 
                     awards=None, 
                     note=None):
        """
        Updates the year, rating, language, country, awards, and note of a movie in the CSV file. 

        This method reads the existing movie data from the CSV file,
        checks if a movie with the given title exists, updates its specified fields if provided,
        and then saves the updated data back to the CSV file.

        Parameters:
        - self (StorageCsv): The instance of the StorageCsv class.
        - title (str): The title of the movie to be updated.
        - year (int, optional): The new release year of the movie. Defaults to None.
        - rating (float, optional): The new rating of the movie. Defaults to None.
        - language (str, optional): The new language of the movie. Defaults to None.
        - country (str, optional): The new country where the movie was produced. Defaults to None.
        - awards (str, optional): The new awards received by the movie. Defaults to None.
        - note (str, optional): The new additional notes about the movie. Defaults to None.

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
            

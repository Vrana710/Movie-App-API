import requests
import os
import random
import pycountry #import countries  # Importing pycountry to convert country names to country codes
from flask import Flask, render_template
from storage.istorage import IStorage
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv('OMDB_API_KEY')

class MovieApp:
    def __init__(self, storage: IStorage):
        """
        Initializes a new instance of MovieApp.

        Parameters:
        storage (IStorage): An instance of a class that implements the IStorage interface.
                            This class is responsible for storing and retrieving movie data.

        Returns:
        None
        """
        self._storage = storage
        self._app = Flask(__name__)


    def _command_list_movies(self): 
        """
        Prints a list of movies along with their details from the storage.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None
        """
        movies = self._storage.list_movies()
        print(f"\n {len(movies)} movies in total")
        if movies:
            for name, details in movies.items():
                print(f"\n{name} ({details['year']}): {details['rating']}")
        else:
            print("\nNo movies found.")

    def _command_add_movie(self):
        """
        Adds a new movie to the storage.

        This function prompts the user to enter a new movie name. 
        It then checks if the movie already exists in the storage.
        If the movie does not exist, it fetches the movie data from 
        the OMDb API using the `_fetch_movie_data` method.
        If the movie data is successfully retrieved, it adds the movie to 
        the storage using the `_storage.add_movie` method.
        If the movie already exists or the movie data is not found, 
        appropriate messages are displayed.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None
        """
        title = input("\nEnter new movie name: ")
        if self._storage.check_if_exists(title):
            print(f"\nMovie {title} already exists")
            return
        data = self._fetch_movie_data(title)
        if data:
            self._storage.add_movie(data["Title"],
                                    data["Year"],
                                    data["imdbRating"],
                                    data["Poster"],
                                    data["Language"], 
                                    data["Country"], 
                                    data["Awards"],
                                    data["imdbID"])  # Add IMDB ID
            print(f"\nMovie {title} added successfully.")
        else:
            print(f"\nMovie {title} not found.")

    @staticmethod
    def _fetch_movie_data(title):
        """
        Fetches movie data from OMDb API.
        
        Args:
            title (str): The title of the movie to fetch. 

        Returns:
            dict: Movie data as returned by OMDb API.
                Returns a dictionary containing the movie details if the movie is found.
                Returns None if the movie is not found or an error occurs during the API request.
        """
        try:
            response = requests.get(f"http://www.omdbapi.com/?"
                                    f"apikey={OMDB_API_KEY}&"
                                    f"t={title}")

            if response.status_code == 200:
                data = response.json()
                if data['Response'] == 'True':
                    year = data["Year"]
                    if "-" in year:
                        year = year.split("-")[0]
                    return {
                        "Title": data["Title"],
                        "Year": year,
                        "imdbRating": data["imdbRating"],
                        "Poster": data["Poster"],
                        "Language": data["Language"],
                        "Country": data["Country"],
                        "Awards": data["Awards"],
                        "imdbID": data["imdbID"]  # Add IMDB ID
                    }
                else:
                    print(f"\nError: {data['Error']}")
            else:
                print("\nError: Could not retrieve data from OMDb API.")
        except requests.RequestException as e:
            print(f"Error: {e}")
        return None


    def _command_delete_movie(self):
        """
        Deletes a movie from the storage.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value. 
              It prints a success message if the movie is deleted,
              or a message indicating that the movie does not exist.
        """
        title = input("\nEnter movie title to delete: ")
        if self._storage.check_if_exists(title):
            self._storage.delete_movie(title)
            print(f"\nMovie {title} deleted successfully.")
        else:
            print(f"\nMovie {title} doesn't exist.")

    
    def _command_update_movie(self):
        """
        Updates the details of an existing movie in the storage.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value. 
              It prints a success message if the movie is updated,
              or a message indicating that the movie does not exist.
        """
        title = input("\nEnter movie title to update: ")
        if self._storage.check_if_exists(title):
            year = input("\nEnter new year of release (or leave blank to keep current): ")
            rating = input("\nEnter new rating (1-10, or leave blank to keep current): ")
            language = input("\nEnter movie language (or leave blank to keep current): ")
            country = input("\nEnter movie country (or leave blank to keep current): ")
            awards = input("\nEnter movie awards (or leave blank to keep current): ")
            note = input("\nEnter movie notes (or leave blank to keep current): ")

            # Parse inputs
            year = int(year) if year else None
            rating = float(rating) if rating else None
            language = language if language else None 
            country = country if country else None
            awards = awards if awards else None 
            note = note if note else None 

            self._storage.update_movie(title, 
                                       year=year, 
                                       rating=rating, 
                                       language=language, 
                                       country=country, 
                                       awards=awards, 
                                       note=note)
            print(f"\nMovie '{title}' updated.")
        else:
            print(f"\nMovie {title} doesn't exist.")

         
    def _command_status(self):
        """
        Prints statistical information about the movies in the storage.

        This function calculates and prints the average rating, median rating,
        best movie(s) by rating, and worst movie(s) by rating.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value. It prints statistical information.
        """
        try:
            movies = self._storage.list_movies()
            ratings = []

            # Extract and convert ratings
            for details in movies.values():
                try:
                    rating = float(details['rating'])
                    ratings.append(rating)
                except ValueError:
                    print(f"\nSkipping invalid rating: {details['rating']}")

            if not ratings:
                print("\nNo valid ratings found to compute statistics.")
                return

            avg_rating = sum(ratings) / len(ratings)
            print(f"\nAverage rating: {avg_rating:.1f}")

            sorted_ratings = sorted(ratings)
            mid = len(sorted_ratings) // 2
            median_rating = (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2 if len(sorted_ratings) % 2 == 0 else sorted_ratings[mid]
            print(f"\nMedian rating: {median_rating:.1f}")

            best_rating = max(ratings)
            worst_rating = min(ratings)

            # Find best and worst movies
            best_movies = [title for title, details in movies.items()
                        if abs(float(details['rating']) - best_rating) < 0.0001]
            worst_movies = [title for title, details in movies.items()
                            if abs(float(details['rating']) - worst_rating) < 0.0001]

            # Print best movies
            print("\nBest movie(s) by rating:")
            if best_movies:
                for movie in best_movies:
                    print(f"\n{movie} ({best_rating})")
            else:
                print("\nNo movies found with the best rating.")

            # Print worst movies
            print("\nWorst movie(s) by rating:")
            if worst_movies:
                for movie in worst_movies:
                    print(f"\n{movie} ({worst_rating})")
            else:
                print("\nNo movies found with the worst rating.")

        except ValueError as error:
            print("\nAn error occurred:", error)


    def _command_random_movie(self):
        """
        Prints a random movie from the storage.

        This function retrieves a list of all movie titles from the storage,
        selects a random title, and prints it. If no movies are found in the storage,
        it prints a message indicating that no movies were found.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value. It prints a random movie title
            or a message indicating that no movies were found.
        """
        movies = list(self._storage.list_movies().keys())
        if movies:
            title = random.choice(movies)
            print(f"\nRandom movie: {title}")
        else:
            print("\nNo movies found.")
    
    
    def _command_search_movie(self):
        """
        Searches for movies in the storage based on a given search query.

        This function prompts the user to enter a search query. 
        It then retrieves a list of all movies from the storage.
        The function searches for movies whose titles contain the   
        search query (case-insensitive).
        If matching movies are found, the function prints their 
        titles, years of release, and ratings.
        If no matching movies are found, the function prints a message 
        indicating that no movies were found.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value. 
        It prints search results or a message indicating that no movies were found.
        """

        query = input("\nEnter search query: ")
        movies = self._storage.list_movies()
        results = {title: details 
                   for title, details in movies.items() 
                        if query.lower() in title.lower()}
        if results:
            for title, details in results.items():
                print(f"\n{title} ({details['year']}): {details['rating']}")
        else:
            print("\nNo matching movies found.")
    
    
    def _command_sort_movies_by_rating(self):
        """
        Sorts and prints the movies in the storage based on their ratings in descending order.

        This function retrieves a list of all movies from 
        the storage using the `_storage.list_movies()` method.
        It then sorts the movies based on their ratings in 
        descending order using the `sorted()` function.
        The `key` parameter of the `sorted()` function is set to a lambda function 
        that extracts the rating from each movie's details.
        The `reverse=True` parameter ensures that the movies are sorted in descending order.

        After sorting the movies, the function iterates over the sorted list and 
        prints each movie's title, year of release, and rating.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value. It prints the sorted list of movies.
        """
        movies = sorted(self._storage.list_movies().items(), 
                        key=lambda x: x[1]['rating'], 
                        reverse=True)
        for title, details in movies:
            print(f"\n{title} ({details['year']}): {details['rating']}")
    
    
    def _command_sort_movies_by_year(self):
        """
        Sorts and prints the movies in the storage based on 
        their release years in descending order.

        This function retrieves a list of all movies from the storage using 
        the `_storage.list_movies()` method.
        It then sorts the movies based on their release years in 
        descending order using the `sorted()` function.
        The `key` parameter of the `sorted()` function is set to a lambda function 
        that extracts the release year from each movie's details.
        The `reverse=True` parameter ensures that the movies are sorted in descending order.

        After sorting the movies, the function iterates over the sorted list and 
        prints each movie's title, year of release, and rating.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value. It prints the sorted list of movies.
        """
        
        # Adjust the sorting to handle year ranges
        def extract_year(movie):
            try:
                return int(movie[1]['year'])
            except ValueError:
                # Handle any non-numeric year cases
                return 0
        
        movies = sorted(self._storage.list_movies().items(), 
                        key=extract_year, 
                        reverse=True)
        for title, details in movies:
            print(f"\n{title} ({details['year']}): {details['rating']}")
    
    
    def _command_filter_movies(self):
        """
        Filters and prints movies from the storage based on a minimum rating.

        This function prompts the user to enter a minimum rating. 
        It then retrieves a list of all movies from the storage.
        The function filters the movies based on their ratings, 
        keeping only those movies with a rating greater than or equal to the minimum rating.
        If matching movies are found, the function prints their titles, 
        years of release, and ratings.
        If no matching movies are found, the function prints a message indicating 
        that no movies were found.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value. 
        It prints filtered movies or a message indicating that no movies were found.
        """
        try:
            min_rating = float(input("\nEnter minimum rating: "))
        except ValueError:
            print("\nInvalid input. Please enter a numeric value for the rating.")
            return

        # Filter movies based on rating
        movies = {
            title: details
            for title, details in self._storage.list_movies().items()
            if details['rating'].replace('.', '', 1).isdigit() 
                        and float(details['rating']) >= min_rating
        }

        if movies:
            for title, details in movies.items():
                print(f"\n{title} ({details['year']}): {details['rating']}")
        else:
            print("\nNo movies found with the specified rating.")


    def _country_to_flag_emoji(self, country_name):
        """
        Converts a country name to a flag emoji.

        Args:
            country_name (str): The name of the country. Multiple country names can be separated by commas.

        Returns:
            str: The corresponding flag emoji(s) along with the country name(s). If a country is not found, 
                a generic flag emoji (🏳️) is used. If multiple countries are provided, the flag emojis 
                are separated by commas.
        """
        result = []
        country_names = country_name.split(',')  # Split the country names if multiple countries are listed
        for name in country_names:
            name = name.strip()
            try:
                # Get the country code from the country name
                country_code = pycountry.countries.lookup(name).alpha_2  # Get the country code from the country name
                flag_emoji = ''.join([chr(ord(char) + 127397) 
                                      for char in country_code])
                result.append(f"{flag_emoji} {name}")  # Format as "🇺🇸 United States"
            except AttributeError:
                result.append(f"🏳️ {name}")  # If country is not found, use a generic flag emoji
        return ', '.join(result)  # Join the formatted strings with commas


    def _command_generate_website(self):
        """
        Generates a static HTML website displaying movie information.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value. It generates a static HTML website.
        """
        movies = self._storage.list_movies()
        movie_grid = ""
        for title, details in movies.items():
            note = details.get('note', 'No notes available')
            flag_country = self._country_to_flag_emoji(details.get('country', 'Unknown'))
            awards = details.get('awards', 'N/A')
            imdb_id = details.get('imdbID', '')  # Get IMDB ID

            # Build the awards section only if the value is not "N/A"
            awards_section = f"<div class='movie-awards'>Awards: {awards}</div>\n" if awards != "N/A" else ""

            movie_grid += (
                f"<li class='movie'>\n"
                f"<a href='https://www.imdb.com/title/{imdb_id}' target='_blank'>\n"  # Link to IMDB page
                f"<img src='{details.get('poster', 'default_poster_url')}' alt='{title} poster' "
                f"class='movie-poster' title='{note}'>\n"
                f"</a>\n"
                f"<div class='movie-info'>\n"
                f"<div class='movie-title'>{title}</div>\n"
                f"<div class='movie-year'>{details.get('year', 'Unknown')}</div>\n"
                f"<div class='movie-language'>{details.get('language', 'Unknown')}</div>\n"
                f"<div class='movie-country'>{flag_country}</div>\n"
                f"{awards_section}"  # Add awards section only if applicable
                "</div>\n"
                "</li>\n"
            )
        
        with open('static/index.html', 'w') as file:
            with open('static/index_template.html', 'r') as template:
                content = template.read()
                content = content.replace('__TEMPLATE_TITLE__', 'My Movie Collection')
                content = content.replace('__TEMPLATE_MOVIE_GRID__', movie_grid)
                file.write(content)
        print("\nWebsite was generated successfully: Name is `index.html`")

    
    def run(self):
        """
        This function runs the main menu loop of the MovieApp.
        It displays a menu with various options for managing movies,
        and handles user input to execute the corresponding commands.

        Parameters:
        self (MovieApp): The instance of the MovieApp class.

        Returns:
        None: This function does not return any value.
        """
        while True:
            print("\n********** My Movies Database **********\n")
            print("Menu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Status")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Movies sorted by year")
            print("10. Filter movies")
            print("11. Generate movies website")
            print("Enter choice (0-11): ", end="")

            choice = input()

            if choice == '0':
                break
            elif choice == '1':
                self._command_list_movies()
            elif choice == '2':
                self._command_add_movie()
            elif choice == '3':
                self._command_delete_movie()
            elif choice == '4':
                self._command_update_movie()
            elif choice == '5':
                self._command_status()
            elif choice == '6':
                self._command_random_movie()
            elif choice == '7':
                self._command_search_movie()
            elif choice == '8':
                self._command_sort_movies_by_rating()
            elif choice == '9':
                self._command_sort_movies_by_year()
            elif choice == '10':
                self._command_filter_movies()
            elif choice == '11':
                self._command_generate_website()
            else:
                print("\nInvalid choice. Please enter a number between 0 and 11.\n")
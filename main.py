import sys
import argparse
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from movie_app.movie_app import MovieApp

def main():
    """
    The main function of the movie application.

    This function initializes the storage based on the file extension,
    creates an instance of the MovieApp with the chosen storage,
    and runs the application.

    Parameters:
    None

    Returns:
    None
    """
    # Specify the actual file path here
    file_path = 'data/data.csv'  # or 'data/data.csv'

    # Check the file extension and instantiate the appropriate storage class
    if file_path.endswith('.json'):
        storage = StorageJson(file_path)
    elif file_path.endswith('.csv'):
        storage = StorageCsv(file_path)
    else:
        raise ValueError("Unsupported file format. Use .json or .csv")

    # Initialize the MovieApp with the chosen storage and run the app
    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    main()

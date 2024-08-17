import argparse
import os
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
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Movie Application')

    # Add an optional argument for the file path
    parser.add_argument(
        'file_path',
        type=str,
        nargs='?',
        default='data/data.json',  # Default file path if none provided
        help='Path to the data file (must be a .csv or .json file)'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Get the file path from arguments
    file_path = args.file_path

    # Get the absolute path based on the current working directory
    absolute_path = os.path.join(os.getcwd(), file_path)

    # Check if the directory exists; create it if it does not
    directory = os.path.dirname(absolute_path)
    if not os.path.exists(directory) and directory:
        print(f"\nWarning: The directory '{directory}' was not found.")
        create_directory = input("\nDo you want to create it? (y/n): ").strip().lower()
        if create_directory == 'y':
            try:
                os.makedirs(directory)
                print(f"\nDirectory '{directory}' created.")
                print(f"\nYour data will be managed in the directory '{directory}'.")
            except Exception as e:
                print(f"\nError creating directory: {e}")
                return
        else:
            print("\nDirectory creation canceled.")
            return

    # Check if the file exists; create it if it does not
    if not os.path.isfile(absolute_path):
        print(f"\nWarning: The file '{absolute_path}' was not found.")
        create_file = input("\nDo you want to create it? (y/n): ").strip().lower()
        if create_file == 'y':
            try:
                if absolute_path.endswith('.json'):
                    with open(absolute_path, 'w') as file:
                        file.write("{}")
                    print(f"\nFile '{absolute_path}' created.")
                    print(f"\nYour data will be managed in the file '{absolute_path}'.")
                elif absolute_path.endswith('.csv'):
                    with open(absolute_path, 'w') as file:
                        file.write("Title,Year,Rating,Poster\n")
                    print(f"\nFile '{absolute_path}' created.")
                    print(f"\nYour data will be managed in the file '{absolute_path}'.")
                else:
                    print("\nUnsupported file format. Use .json or .csv")
                    return
            except Exception as e:
                print(f"\nError creating file: {e}")
                return
        else:
            print("\nFile creation canceled.")
            return

    # Check the file extension and instantiate the appropriate storage class
    try:
        if absolute_path.endswith('.json'):
            storage = StorageJson(absolute_path)
        elif absolute_path.endswith('.csv'):
            storage = StorageCsv(absolute_path)
        else:
            raise ValueError("\nUnsupported file format. Use .json or .csv")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Initialize the MovieApp with the chosen storage and run the app
    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    main()

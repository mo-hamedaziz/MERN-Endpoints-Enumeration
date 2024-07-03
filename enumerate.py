import os
import re
import argparse
from tqdm import tqdm

# Function to extract routes from a file
def extract_routes_from_file(file_path):
    routes = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for index, line in enumerate(lines, start=1):
                # Regex to match Express route definitions
                match = re.match(r'\s*app\.(get|post|put|delete|patch)\s*\(\s*\'(/[\w/{}:-]*)\'', line)
                if match:
                    method = match.group(1).upper()
                    route = match.group(2)
                    routes.append({
                        'method': method,
                        'route': route,
                        'file': file_path,
                        'line': index
                    })
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return routes

# Function to enumerate all routes in a directory
def enumerate_routes(directory, verbose=False):
    all_routes = []
    files_list = []

    # Walk through the directory to get all .js files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                files_list.append(os.path.join(root, file))

    if verbose:
        print(f"Found {len(files_list)} JavaScript files. Enumerating routes...")

    # Use tqdm to display a progress bar
    for file_path in tqdm(files_list, desc="Enumerating routes"):
        routes = extract_routes_from_file(file_path)
        all_routes.extend(routes)

    return sorted(all_routes, key=lambda x: x['route'])  # Sort routes by route path

# Function to check if the directory is a MERN backend
def is_mern_backend(directory):
    package_json_path = os.path.join(directory, 'package.json')
    if not os.path.exists(package_json_path):
        return False
    try:
        with open(package_json_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if '"express"' in content or '"koa"' in content or '"hapi"' in content:
                return True
    except Exception as e:
        print(f"Error reading package.json: {e}")
    return False

# Function to export routes to a file
def export_routes_to_file(routes, file_name, base_directory):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            for route in routes:
                relative_path = os.path.relpath(route['file'], base_directory)
                file.write(f"{route['method']} {route['route']} - Defined in {relative_path} at line {route['line']}\n")
        print(f"You can find the results in {file_name}")
    except Exception as e:
        print(f"Error exporting routes to {file_name}: {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Enumerate REST API endpoints in a MERN backend.")
    parser.add_argument('directory', type=str, help='Path to the backend directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    parser.add_argument('--export', type=str, metavar='file_name', help='Export routes to a text file')
    parser.add_argument('-y', '--yes', action='store_true', help='Automatically confirm all prompts with yes')
    args = parser.parse_args()

    # Automatic confirmation if -y or --yes option is provided
    if args.yes:
        confirm = 'y'
    else:
        # Confirm directory
        print(f"Checking if '{args.directory}' is a valid MERN backend directory...")
        if not os.path.exists(args.directory):
            print(f"Error: The directory '{args.directory}' does not exist.")
            return

        if not is_mern_backend(args.directory):
            print(f"Error: The directory '{args.directory}' does not appear to be a MERN backend.")
            return

        # Confirm to proceed
        confirm = input(f"The directory '{args.directory}' is a valid MERN backend. Do you want to proceed with enumerating the routes? (Y/n): ").strip().lower()

    if confirm not in ['', 'y']:
        print("Operation cancelled.")
        return

    # Enumerate and print the routes
    print("Enumerating routes, please wait...")
    routes = enumerate_routes(args.directory, args.verbose)
    
    # Sort routes by method and then by route path
    sorted_routes = sorted(routes, key=lambda x: (x['method'], x['route']))

    if sorted_routes:
        if args.export:
            export_routes_to_file(sorted_routes, args.export, args.directory)
        else:
            print("\nFound the following routes:")
            for route in sorted_routes:
                if args.verbose:
                    relative_path = os.path.relpath(route['file'], args.directory)
                    print(f"{route['method']} {route['route']} - Defined in {relative_path} at line {route['line']}")
                else:
                    print(route['method'], route['route'])
    else:
        print("No routes found.")

if __name__ == '__main__':
    main()


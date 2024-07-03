# REST API Endpoint Enumerator

## Description
This Python script is designed to enumerate and list all REST API endpoints defined in JavaScript files within a MERN (MongoDB, Express.js, React, Node.js) backend directory. It parses Express route definitions (`app.get`, `app.post`, etc.) and outputs detailed information about each route, including HTTP method, route path, and file location.

## Features
- Enumerates all REST API endpoints within a MERN backend directory.
- Supports automatic confirmation (`-y` or `--yes`) to bypass prompts.
- Optionally exports enumerated routes to a text file.
- Provides verbose output option (`-v` or `--verbose`) for detailed route information.

## Requirements
- Python 3.x
- tqdm==4.64.1

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>

2. Install dependencies using pip:
   ```bash
   pip install -r requirements.txt

## Usage
  ```bash
  python <script_name>.py <directory> [-v] [--export <file_name>] [-y]
  ```

## Arguments
- directory: Path to the MERN backend directory.
- -v, --verbose: Increase output verbosity.
- --export <file_name>: Export enumerated routes to a text file.
- -y, --yes: Automatically confirm all prompts with yes.

## Example of usage
- Enumerate routes in a MERN backend directory:
  ```bash
  python enumerate.py /path/to/backend
  ```
- Export enumerated routes to a file:
  ```bash
  python enumerate.py /path/to/backend --export routes.txt
  ```

## Author
Mohamed Aziz Bchini - M4dz






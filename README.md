# PyKotlin-Channel-Mapper
PyKotlin Channel Mapper: Python program to extract essential YouTube channel data. Reduce JSON response, generate Kotlin code for Channel object with video details. Streamline YouTube API integration.

![Screenshot 2023-06-03 182311](https://github.com/avill2022/PyKotlin-Channel-Mapper/assets/105819329/1b962536-83fc-426a-9d88-27f67ffd578f)

# PyTube Channel Extractor

PyTube Channel Extractor is a Python program designed to simplify and extract relevant information from the YouTube API.

## Description
The program takes an ID channel as input and sends a request to the YouTube API. It retrieves a JSON response, reduces the data to include only the necessary information, and generates a Kotlin code snippet. This code snippet demonstrates how to create a Channel object in Kotlin, complete with a list of videos and their associated information.

## Features
- Simplifies YouTube API data
- Generates Kotlin code for Channel object with video details
- Streamlines YouTube API integration

## Setting Up System Variable
To use the YouTube API, you need to set up a system variable to store your API key. Follow the steps below:

1. Copy your YouTube API key from the [Google Developers Console](https://console.developers.google.com/).
2. Open your system's environment variable settings.
   - **Windows**: Go to Control Panel > System and Security > System > Advanced system settings > Environment Variables.
   - **Mac/Linux**: Open a terminal and edit your `.bashrc` or `.bash_profile` file.
3. Add a new system variable named `YOUTUBE_API_KEY` and set its value to your API key.

**Example (Windows):**
Variable name: YOUTUBE_API_KEY
Variable value: YOUR_API_KEY


**Example (Mac/Linux):**
bash
export YOUTUBE_API_KEY=YOUR_API_KEY
Note: Replace YOUR_API_KEY with your actual YouTube API key.

Save the changes and restart your terminal or command prompt for the new variable to take effect.
Adding the YouTube API Key
To add your YouTube API key in the PyTube Channel Extractor project, follow these steps:

Open the config.py file in the project directory.

Locate the API_KEY variable.

Replace the placeholder value with your YouTube API key:

python
Copy code
API_KEY = "YOUR_API_KEY"

## Getting Started
1. Clone the repository: `git clone https://github.com/your-username/PyTube-Channel-Extractor.git](https://github.com/avill2022/PyKotlin-Channel-Mapper.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the program: `python main.py`

## Usage
1. Provide the ID channel as input.
2. The program will send a request to the YouTube API and retrieve the JSON response.
3. The JSON response will be reduced and simplified to include only essential information.
4. A Kotlin code snippet will be generated, demonstrating the creation of a Channel object with video details.


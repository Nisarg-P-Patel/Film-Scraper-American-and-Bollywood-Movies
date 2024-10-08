# -*- coding: utf-8 -*-
"""Web Scrapper .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xnXBN85MTQ8BAalAmJCQjaQKc0Oxq5up
"""

!pip install ipywidgets

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

# Define the dataset location
current_dir = os.getcwd()  # Get the current working directory
dataset_location = os.path.realpath(os.path.join(current_dir, "Datasets"))  # Create an absolute path for the 'Datasets' directory
os.makedirs(dataset_location, exist_ok=True)  # Create the 'Datasets' directory if it doesn't already exist

def america_pre_process(dataset_location, url):
    # Send request to fetch the content of the Wikipedia page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Define a list to hold all movie data
    movies_list = []

    # Find all tables that list movies by quarter
    tables = soup.find_all('table', class_='wikitable')

    # Iterate over each table (each table is a quarter of the year)
    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip the header row

        # Process each row in the table
        for row in rows:
            cols = row.find_all('td')

            # Check if the row has the correct number of columns
            if len(cols) >= 4:
                # Extract relevant details from the columns
                movie_details = {
                    'Title': cols[0].get_text(strip=True),           # Extract movie title
                    'Production Company': cols[1].get_text(strip=True),  # Extract production company
                    'Cast and Crew': cols[2].get_text(strip=True),      # Extract cast and crew details
                    'Ref': cols[3].get_text(strip=True)                  # Extract reference information
                }
                # Add the movie details to the list
                movies_list.append(movie_details)

    # Create a DataFrame from the collected movie data
    df = pd.DataFrame(movies_list)

    # Filter out rows where 'Ref' contains a dollar sign
    filtered_df = df[~df['Ref'].str.contains('\$', na=False)]

    # Define a mask for rows that meet specific conditions
    mask = (
        filtered_df['Ref'].notna() &                           # 'Ref' should not be NaN
        ~filtered_df['Ref'].str.startswith('[') &              # 'Ref' should not start with '['
        ~filtered_df['Ref'].str.endswith(']') &                # 'Ref' should not end with ']'
        filtered_df['Title'].str.isnumeric() == True          # 'Title' should not be numeric
    )

    # Create a copy of the DataFrame to avoid SettingWithCopyWarning
    df_shifted = filtered_df.copy()

    # Apply the mask to filter DataFrame
    masked_df = df_shifted[mask]

    # Delete the first column (assumed to be the index)
    masked_df = masked_df.drop(columns=['Title'])

    # Rename the columns for clarity
    masked_df.columns = ['Title', 'Production Company', 'Cast and Crew']

    # Remove the rows in filtered_df that met the mask condition and drop the 'Ref' column
    df = filtered_df[~mask].drop(columns=['Ref'])

    # Merge the original DataFrame (without masked rows) and the masked DataFrame
    merged_df = pd.concat([df, masked_df], ignore_index=True)

    # Define the directory path
    directory_path = dataset_location +'/HollyWood/'

    # Check if the directory exists
    if not os.path.exists(directory_path):
        # Create the directory if it does not exist
        os.makedirs(directory_path)

    # Save the merged DataFrame to a CSV file
    merged_df.to_csv(directory_path + url.split('/')[-1] + '.csv', index=False)

    print("Data location -> ", directory_path)

# Example usage
# america_pre_process("https://en.wikipedia.org/wiki/List_of_American_films_of_2020")

def bollywood_pre_process(dataset_location, url):
    # Send a GET request to fetch the content of the Wikipedia page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Define a list to store movie data extracted from the page
    movies_list = []

    # Find all tables with class 'wikitable' that list movies on the page
    tables = soup.find_all('table', class_='wikitable')

    # Iterate over each table found on the page
    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip the first row (header)

        # Process each row in the table
        for row in rows:
            cols = row.find_all('td')

            # Check if the row has enough columns (at least 5) to extract meaningful data
            if len(cols) >= 5:
                # Some rows might have an extra numeric column, we handle that here
                if cols[1].get_text(strip=True).isnumeric():
                    cols = cols[1:]  # Remove the extra numeric column

                # Extract movie details like title, director, cast, studio, and reference
                movie_details = {
                    'Title': cols[0].get_text(strip=True),      # Movie title
                    'Director': cols[1].get_text(strip=True),   # Director(s)
                    'Cast': cols[2].get_text(strip=True),       # Cast
                    'Studio': cols[3].get_text(strip=True),     # Production company (studio)
                    'Ref': cols[4].get_text(strip=True)         # Reference information (optional)
                }

                # Add the movie details to the list
                movies_list.append(movie_details)

    # Convert the list of movie data into a pandas DataFrame for easy processing
    df = pd.DataFrame(movies_list)

    # Filter out rows where the 'Studio' contains '$' symbol, likely erroneous entries
    filtered_df = df[~df['Studio'].str.contains('\$', na=False)]

    # Update the DataFrame to use only the filtered data
    df = filtered_df

    # Define a condition (mask) to handle invalid rows where reference is missing or incorrect
    mask = (
        df['Ref'].notna() &                             # Reference is not empty
        ~df['Ref'].str.startswith('[') &                # Reference doesn't start with '['
        ~df['Ref'].str.endswith(']') &                  # Reference doesn't end with ']'
        df['Title'].str.isnumeric() == True             # Title is not a numeric value
    )

    # Create a copy of the DataFrame to avoid potential warnings
    df_shifted = df.copy()

    # Apply the mask to extract rows that meet the condition
    masked_df = df_shifted[mask]

    # Drop the 'Title' column from the masked DataFrame
    masked_df = masked_df.drop(columns=['Title'])

    # Rename the columns to match the original structure after the shift
    masked_df.columns = ['Title', 'Director', 'Cast', 'Studio']

    # Remove rows that meet the mask condition from the original DataFrame and drop 'Ref' column
    df = df[~mask].drop(columns=['Ref'])

    # Merge the cleaned DataFrames (original and masked) into one
    merged_df = pd.concat([df, masked_df], ignore_index=True)

    # Define the directory path to save the CSV file
    directory_path = dataset_location + '/BollyWood/'

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Save the merged DataFrame to a CSV file named after the last part of the URL
    merged_df.to_csv(directory_path + url.split('/')[-1] + '.csv', index=False)

    print("Data location -> ", directory_path)

# Example usage
# bollywood_pre_process("https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2020")

def scrape_wikipedia_movies(dataset_location, year, industry):
    """
    Scrape movie data from Wikipedia based on the given year and film industry.

    Parameters:
    dataset_location (str): The location to store the dataset.
    year (int): The year for which movies are to be scraped.
    industry (str): The film industry to target, either 'American' or 'Bollywood'.

    If the industry is 'American', it scrapes data from the Wikipedia page for American films of that year.
    If the industry is 'Bollywood', it scrapes data from the Wikipedia page for Hindi films of that year.
    Calls appropriate preprocessing functions based on the industry.
    """

    # For American films, generate the Wikipedia URL for that year and call the preprocessing function.
    if industry == "American":
        url = f"https://en.wikipedia.org/wiki/List_of_American_films_of_{year}"
        america_pre_process(dataset_location, url)

    # For Bollywood (Hindi) films, generate the Wikipedia URL for that year and call the preprocessing function.
    elif industry == "Bollywood":
        url = f"https://en.wikipedia.org/wiki/List_of_Hindi_films_of_{year}"
        bollywood_pre_process(dataset_location, url)

    # If the industry is neither American nor Bollywood, return an empty list (no data to scrape).
    else:
        return []

import ipywidgets as widgets
from IPython.display import display
from tqdm import tqdm

# Define the function that triggers the scraping
def run_scraper(start_year, current_year, industries):
    """
    Scrapes movies for the specified year range and industries.

    Parameters:
    start_year (int): The starting year for scraping.
    current_year (int): The ending year for scraping.
    industries (list): List of film industries to scrape (e.g., 'American', 'Bollywood').

    For each year in the range, it calls the scrape function for each industry.
    """
    dataset_location = '/content/Datasets'  # Predefined path for saving scraped data

    for year in tqdm(range(start_year, current_year + 1)):
        for industry in industries:
            scrape_wikipedia_movies(dataset_location, year, industry)

    print("Scraping completed.")

# Create interactive widgets for selecting year range and industry
start_year_widget = widgets.IntSlider(value=2020, min=2000, max=2023, step=1, description='Start Year')
end_year_widget = widgets.IntSlider(value=2024, min=2001, max=2024, step=1, description='End Year')

# Checkbox widgets to select which industries to scrape
industry_widget = widgets.SelectMultiple(
    options=["American", "Bollywood"],
    value=["American", "Bollywood"],
    description="Industries",
    disabled=False
)

# Create an output area for warning or success messages
output_area = widgets.Output()

# Create a button to start the scraping process
scrape_button = widgets.Button(description="Start Scraping")

# Define what happens when the button is clicked
def on_button_click(b):
    """
    This function is triggered when the 'Start Scraping' button is clicked.
    It retrieves the selected values from the widgets and checks if the end year is valid.
    It also ensures only one industry is selected.
    """
    start_year = start_year_widget.value
    current_year = end_year_widget.value
    industry = industry_widget.value  # Only one industry is allowed

    with output_area:
        output_area.clear_output()  # Clear any previous output
        # Check if the end year is greater than or equal to the start year
        if current_year >= start_year:
            print(f"Scraping movies from {start_year} to {current_year} for the {industry} industry...")
            run_scraper(start_year, current_year, industry)
        else:
            print(f"Error: End year ({current_year}) must be greater than or equal to the start year ({start_year}).")

# Link the button click event to the function
scrape_button.on_click(on_button_click)

# Display the widgets in the output
display(start_year_widget, end_year_widget, industry_widget, scrape_button, output_area)


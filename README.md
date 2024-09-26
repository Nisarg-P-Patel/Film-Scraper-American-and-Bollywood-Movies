# Film-Scraper-American-and-Bollywood-Movies

Overview
--------

The **Movie Data Scraper** is a Python-based web scraping tool designed to automatically collect and organize movie data from Wikipedia for American and Bollywood films released from 2020 to 2024. This project utilizes libraries like BeautifulSoup for HTML parsing and pandas for data manipulation, providing an easy way to gather information on movies, including titles, directors, cast, production companies, and references.

Features
--------

*   **Multi-Industry Support**: Scrapes data for both American and Bollywood films.
    
*   **Data Cleaning**: Filters out erroneous entries and cleans the dataset for accuracy.
    
*   **CSV Export**: Saves the collected movie data into CSV files for easy access and analysis.
    
*   **User-Friendly Interface**: Offers an interactive widget interface for selecting the year range and film industry.
    

Requirements
------------

Before running the scraper, ensure you have the following libraries installed:

` pip install requests beautifulsoup4 pandas tqdm ipywidgets   `

Getting Started
---------------

### Running the Scraper

1.  Open the Jupyter Notebook (Web\_Scraper.ipynb) in your favorite environment (like Jupyter Notebook or Google Colab).
    
2.  Adjust the year range and select the film industries (American and Bollywood) using the provided interactive widgets.
    
3.  Click on the **Start Scraping** button to initiate the data collection process.
    

### Data Output

The scraped data will be saved in the following directory structure:

Datasets/Hollywood/ CSV files

Datasets/Bollywood/ CSV files


Example Usage
-------------

To scrape data for a specific year, you can use the following example URLs:

*   American Films: [List of American films of 2020](https://en.wikipedia.org/wiki/List_of_American_films_of_2020)
    
*   Bollywood Films: [List of Hindi films of 2020](https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2020)
    

Contributing
------------

Contributions are welcome! If you have suggestions for improvements or want to add features, feel free to open an issue or submit a pull request.

Acknowledgments
---------------

*   Special thanks to the developers of the libraries used in this project, especially BeautifulSoup and pandas, for their powerful web scraping and data manipulation capabilities.

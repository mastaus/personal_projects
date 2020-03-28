This repository hosts my work on the project to track Amsterdam (Netherlands) housing market prices, analyze the trends and get alerted when properties that match our criteria show up on the market :house:

For now the scraping is done semi manually (meaning I have to initialize the scraping and solve reCAPTCHAs manually). The data is then stored in a pickle file before going into a database.

The data is stored in a PostgreSQL database :books: :key:

*Please note that some of the code in this repo reads credentials from the .env file, which is not on the remote repo (for obvious reasons), please replace those variables with your own credentials, if cloning this repo.
The current .env file contains:
google_profile, username, secret_ms, secret_f, secret_g, webdriver_loc, url, login_url, logout_url*

## To Do list:

1. Adjust Address column to contain full address (concat Title and Address columns) :thumbsup:
2. Convert Asking price and Asking price per m² into **integer** values :thumbsup:
3. Separate VVE flag from the monthly contribution (while converting the latter into an integer) :thumbsup:
4. Convert Year of construction into an integer :thumbsup:
5. Convert living area, exterior area and volume columns into integers :thumbsup:
6. Convert "Listed since" field into a date - **not possible because I didn't record the scraped date. The original field shows the date or number of weeks or number of months from the current date**
7. Separate rooms field and bedrooms field into two different columns (both converted into integers) :thumbsup:
8. Create bathtub flag
9. Separate number of bathrooms and toilets into different columns :thumbsup:
10. Separate number of baths, showers and toilets
11. Create python files to store functions into (rather than in jupyter notebook directly) and simply import them
12. 

# Open Corporates Scraper

A html content scraper written in Python using BeautifulSoup, Selenium and ChromeDriverManager to scrape company and employee data from www.opencorporates.com and store the information in a .csv file.

## Files
* `main.py`: the driver code to start the scraper 
* `scraper_officer.py`: the module to scrape officer data
* `scraper_company.py`: the module to scrape company data

## How to run the scraper? 
1. Run `main.py`, which will prompt the user to either type '1' for scraping company data or '2' for officer data. 
2. `main.py` will execute the corresponding module according to user's input
3. Both scrapers `scraper_officer.py` and `scraper_company.py` will allow user to keep scraping until "QUIT" is entered.
4. The output will be stored in `scraper_company_output.csv` for company data and `scraper_officer_output.csv` for officer data. 

## Note 
You might need to install some packages and modules the scrapers depend on. 
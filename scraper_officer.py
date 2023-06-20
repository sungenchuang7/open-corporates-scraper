import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd
import time

header = [
    "Person's Name",
    "Company Name",
    "Company Link",
    "Name",
    "Address",
    "Position",
    "Start Date",
    "Other Officers In Company"
]

df = pd.DataFrame(columns = header)

data = {}

# Set up Chrome driver options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without UI)

# Initialize Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Read https://opencorporates.com/companies/us_de/5273346
driver.get("https://opencorporates.com")

accept_cookies_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cky-btn-accept")))
accept_cookies_button.click()

# Select officer search mode
officer_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "officerRadio")))
officer_button.click()

# driver.find_element(By.NAME, “).send_keys(“query” + Keys.ENTER)
search_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "oc-home-search_button")))

# Find the search bar and get rid of the default search value
search_bar = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "oc-home-search_input")))
search_bar.clear()
# Prompt the user for input 

user_input = input("Please enter the name of the officer of which you'd like to scrape data: ")
# Fill out the search bar with user input 
search_bar.send_keys(user_input)

# Click the search button 
search_button.click()

url_search_result = driver.current_url

driver.get(url_search_result)

# Wait until the desired elements are present or visible on the page
wait = WebDriverWait(driver, 20)  # Maximum wait time of 10 seconds
search_results_page_obj = wait.until(EC.presence_of_element_located((By.ID, "results")))


# Create a BeautifulSoup object
soup = BeautifulSoup(driver.page_source, features="lxml")

# Check how many officers match the search
number_of_officers_found = soup.find('div', {'class': 'span7'}).find('h2').get_text()
print(number_of_officers_found)

# If none, end the program
if number_of_officers_found == '\nFound 0 officers\n':
    print("Sorry. There's no matching result for the officer you searched for.")
    sys.exit()

first_li = soup.find('ul', {'class': 'officers unstyled'}).find('li')
print(first_li)
# Get the URL of the person
url = first_li.find('a').get('href')
print(url)

driver.get("https://opencorporates.com" + url)

print("reached here1")
soup = BeautifulSoup(driver.page_source, features="lxml")

officer_name_obj = soup.find('h1')
officer_name_string = officer_name_obj.text.strip()
print("officer_name: " + officer_name_string)

data["Person's Name"] = officer_name_string

company_obj = soup.find('dd', class_='company')
company_name_string = company_obj.find('a').text.strip()
company_url_string = company_obj.find('a')['href']
print("company_name: " + company_name_string)
print("company_url: " + company_url_string)

data["Company Name"] = company_name_string
data["Company Link"] = "https://opencorporates.com" + company_url_string

name_obj = soup.find('dd', class_='name')
name_string = name_obj.find('a').text.strip()
print("name: " + name_string)

data["Name"] = name_string

### LOG-IN REQUIRED TO ACCESS ADDRESS DATA ###
data["Address"] = "N/A"

position_obj = soup.find('dd', class_='position')
position_string = position_obj.text.strip()

data["Position"] = position_string

start_date_string = "DEFAULT_VALUE"
start_date_obj = soup.find('dd', class_='start_date')
if start_date_obj is None:
    start_date_string = "N/A"
else:
    start_date_string = start_date_obj.text.strip()

data["Start Date"] = start_date_string

ul_element = soup.find('ul', class_='officers')
officers = ul_element.find_all('li')


temp_header = [
    "Name",
    "Title",
    "Date"
]

officers_df = pd.DataFrame(columns=temp_header)


for officer in officers: 

    officer_dict = {}

    name_element = officer.find('a', class_='officer')
    name = name_element.text.strip()

    title = name_element.find_next_sibling(text=True).strip(", ")

    date_element = soup.find('span', class_='start_date')
    date = date_element.text.strip()

    print("Name:", name)
    print("Title:", title)
    print("Date:", date)

    officer_dict["Name"] = name
    officer_dict["Title"] = title
    officer_dict["Date"] = date

    officers_df = officers_df.append(officer_dict, ignore_index=True)

data["Other Officers In Company"] = officers_df

df = df.append(data, ignore_index=True)

# print(df)

df.to_csv('scraper_officer_output.csv', index=False)

# Quit the driver
driver.quit()

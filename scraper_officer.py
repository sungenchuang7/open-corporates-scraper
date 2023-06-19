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
import helpers

def get_filing_soup_from_url(url):
    chrome_options_helper = Options()
    chrome_options_helper.add_argument("--headless")  # Run Chrome in headless mode (without UI)
    # wait_helper = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
    # filing_date_helper = wait_helper.until(EC.presence_of_element_located((By.CLASS_NAME, "filing_date")))
    driver_helper = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    print("URL: " + url)
    driver_helper.get(url)
    wait_helper = WebDriverWait(driver_helper, 20)  # Maximum wait time of 10 seconds
    filing_date = wait_helper.until(EC.presence_of_element_located((By.CLASS_NAME, "filing_date")))
    print("HELPER: filing_date: " + filing_date.text)

    soup_helper = BeautifulSoup(driver_helper.page_source, features="lxml")
    # print(soup)
    return soup_helper


TEST_OFFICER_1 = "file:///Users/seanchuang/Desktop/take-home-tasks/TRACT/officer1.html"




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

# input1 = input("Do you want to scrape data about a company or about an officer? \nEnter 1 for company and 2 for officer.")




# Set up Chrome driver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without UI)

# Initialize Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Read https://opencorporates.com/companies/us_de/5273346
driver.get(TEST_OFFICER_1)

# Wait until the desired elements are present or visible on the page
wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
company_number = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "address")))

# Create a BeautifulSoup object
soup = BeautifulSoup(driver.page_source, features="lxml")

# Print the text of the element
# print(company_number.text)

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
data["Company Link"] = company_url_string

name_obj = soup.find('dd', class_='name')
name_string = name_obj.find('a').text.strip()
print("name: " + name_string)

data["Name"] = name_string

### LOG-IN REQUIRED TO ACCESS ADDRESS DATA ###
data["Address"] = "LOG-IN REQUIRED FOR ADDRESS"

position_obj = soup.find('dd', class_='position')
position_string = position_obj.text.strip()

data["Position"] = position_string

start_date_obj = soup.find('dd', class_='start_date')
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

df.to_csv('officer_output.csv', index=False)

# Quit the driver
driver.quit()

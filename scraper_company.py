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


TEST_PAGE_1 = "file:///Users/seanchuang/Desktop/take-home-tasks/TRACT/page1.html"
TEST_PAGE_1_FILING1 = "file:///Users/seanchuang/Desktop/take-home-tasks/TRACT/page1_filing1.html"



header = [
    'Company Name',
    'Company Number',
    'Status',
    'Incorporation Date',
    'Dissolution Date',
    'Company Type',
    'Jurisdiction',
    'Business Number',
    'Registry Page',
    'Recent Filings',
    'Source'
    'Latest Events'
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
driver.get(TEST_PAGE_1)

# Wait until the desired elements are present or visible on the page
wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
company_number = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "company_number")))

# Create a BeautifulSoup object
soup = BeautifulSoup(driver.page_source, features="lxml")

# Print the text of the element
# print(company_number.text)

company_name_obj = soup.find("h1", class_="wrapping_heading")
company_name_string = company_name_obj.text.strip()
print("company_name: " + company_name_string)


company_number_obj = soup.find("dd", class_="company_number")
company_number_string = company_number_obj.text
print("company_number: " + company_number_string)

status_obj = soup.find("dd", class_="status")
status_string = status_obj.text.strip()
print("status: " + status_string)

# Same for incorporation_date
incorporation_date_obj = soup.find("dd", class_="incorporation_date")
incorporation_date_string = incorporation_date_obj.text
print("incorporation_date: " + incorporation_date_string)
# print(type(incorporation_date_string))

dissolution_date_obj = soup.find("dd", class_="dissolution date")
dissolution_date_string = "default_string"
if dissolution_date_obj is not None: 
    dissolution_date_string = dissolution_date_obj.text
    print("dissolution_date: " + dissolution_date_string)
else:
    dissolution_date_string = "None"
    print("dissolution_date: " + dissolution_date_string)


# company_type
company_type_obj = soup.find("dd", class_="company_type")
company_type_string = company_type_obj.text.strip()
print("company_type: " + company_type_string)

# jurisdiction
jurisdiction_obj = soup.find("dd", class_="jurisdiction")
jurisdiction_string = jurisdiction_obj.text.strip()
print("jurisdiction: " + jurisdiction_string)

# business number
business_number_obj = soup.find("dd", class_="business_number")
business_number_string = business_number_obj.text.strip()
print("business_number: " + business_number_string)

# registry page
registry_page_obj = soup.find("dd", class_="registry_page")
registry_page_string = registry_page_obj.text.strip()
print("registry_page: " + registry_page_string)

print("--------------------FILINGS INFORMATION-------------------------")

list_of_filings = []
filings = soup.find_all("a", class_="filing")
for filing in filings:
    filing_list = []
    filing_name_string = filing.text
    filing_url_string = filing.get("href")
    print("filing_name: " + filing_name_string)
    print("filing_url: " + filing_url_string)
    filing_soup = get_filing_soup_from_url(TEST_PAGE_1_FILING1) # debug
    # print(filing_soup)
    filing_date = filing_soup.find("dd", class_="filing_date")
    if filing_date is None:
        print("shit happened!")
    filing_date_string = filing_date.text.strip()
    print("filing_date: " + filing_date_string)
    filing_number = filing_soup.find("dd", class_="filing_number truncate")
    filing_number_string = filing_number.text.strip()
    print("filing_number: " + filing_number_string)
    filing_type = filing_soup.find("dd", class_="filing_type")
    filing_type_string = filing_type.text.strip()
    print("filing_type_string: " + filing_type_string)
    filing_code = filing_soup.find("dd", class_="filing_code")
    filing_code_string = filing_code.text.strip()
    print("filing_code_string: " + filing_code_string)

    
    name_tuple = ("Filing Name", filing_name_string)
    url_tuple = ("Filing URL", filing_url_string)
    date_tuple = ("Filing Date", filing_date_string)
    type_tuple = ("Filing Type", filing_type_string)
    code_tuple = ("Filing Code", filing_code_string)

    filing_list.append(name_tuple)
    filing_list.append(url_tuple)
    filing_list.append(date_tuple)
    filing_list.append(type_tuple)
    filing_list.append(code_tuple)

    list_of_filings.append(filing_list)

print("--------------------------------------------------------------")

source_obj = soup.find("span", class_="publisher")
source_string = source_obj.text.strip()
print("source: " + source_string)

list_of_events = []



events = soup.find_all("div", class_="event-timeline-row")

for event in events:
    event_list = []
    # Find the <dt> element within the event
    date_element = event.find("dt")
    # Extract the date from the enclosed text
    date_string = date_element.text.strip()
    print("event date: " + date_string)
    # Find the <dd> element within the event
    description_element = event.find("dd") 
    # Extract the text from the <a> element within the <dd> element
    description_string = description_element.find("a").text.strip()
    print("event description: " + description_string)

    date_tuple = ("Event Date", date_string)
    description_tuple = ("Event Description", description_string)

    event_list.append(date_tuple)
    event_list.append(description_tuple)

    list_of_events.append(event_list)


data['Company Name'] = company_name_string
data['Company Number'] = company_number_string
data['Status'] = status_string
data['Incorporation Date'] = incorporation_date_string
data['Dissolution Date'] = dissolution_date_string
data['Company Type'] = company_type_string
data['Jurisdiction'] = jurisdiction_string
data['Business Number'] = business_number_string
data['Registry Page'] = registry_page_string
data['Recent Filings'] = list_of_filings
data['Source'] = source_string
data['Latest Events'] = list_of_events


df = df.append(data, ignore_index=True)

print(df)

df.to_csv('output_company.csv', index=False)

# Quit the driver
driver.quit()

## Convert tag data type to string
## Store the heading and the data (status, incorporation date, ...) into a dataframe
## Write the dataframe into a csv file. 

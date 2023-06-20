import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.common.keys import Keys
import sys


#################### HELPER FUNCTIONS ###################
# Given a url, this function returns a soup for filing data 
def get_filing_soup_from_url(url):
    chrome_options_helper = Options()
    chrome_options_helper.add_argument("--headless")  # Run Chrome in headless mode (without UI)
    # wait_helper = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
    # filing_date_helper = wait_helper.until(EC.presence_of_element_located((By.CLASS_NAME, "filing_date")))
    driver_helper = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options_helper)
    print("URL: " + url)
    driver_helper.get(url)
    wait_helper = WebDriverWait(driver_helper, 20)  # Maximum wait time of 10 seconds
    filing_date = wait_helper.until(EC.presence_of_element_located((By.CLASS_NAME, "filing_date")))
    print("HELPER: filing_date: " + filing_date.text)

    soup_helper = BeautifulSoup(driver_helper.page_source, features="lxml")
    # print(soup)
    return soup_helper

# Helper function to print ......
def print_loading(string):
    print(string, end='', flush=True)  # Print the initial string without a newline character
    for _ in range(5):  # Repeat 5 times for a total of 10 periods
        time.sleep(1)  # Delay for 1 second
        print('.', end='', flush=True)  # Print a period without a newline character
    print()

#################### MAIN SCRIPT #######################

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

while True:
    # Set up Chrome driver options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without UI)

    # Initialize Chrome driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Read https://opencorporates.com/
    driver.get("https://opencorporates.com/")

    # First find accept cookies button and click it
    accept_cookies_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cky-btn-accept")))
    accept_cookies_button.click()

    # Find the search button
    search_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "oc-home-search_button")))

    # Find the search bar
    search_bar = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "oc-home-search_input")))

    # Prompt the user for input 
    user_input = input("Please enter the name of the company of which you'd like to scrape data, or type 'QUIT' to exit the program: ")

    if user_input.strip().lower() == "quit":
        break

    # Fill out the search bar with user input 
    search_bar.send_keys(user_input)

    # Click the search button 
    search_button.click()

    # Read the search result page
    url_company_search_result = driver.current_url
    driver.get(url_company_search_result)

    # Wait for API to send response
    wait = WebDriverWait(driver, 20)  # Maximum wait time of 10 seconds
    temp = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oc-header-search__field")))

    # Update soup
    soup = BeautifulSoup(driver.page_source, features="lxml")

    # Check how many companies match the search query
    number_of_companies_found = soup.find('div', {'class': 'span7'}).find('h2').get_text()
    print(number_of_companies_found)

    # If none, end the program
    if number_of_companies_found == '\nFound 0 companies\n':
        print("Sorry. There's no matching result for the company you searched for.")
        continue

    # Find the first <li> tag under the <ul> tag
    first_li = soup.find('ul', {'id': 'companies'}).find('li')

    # Get the URL of the company
    url = first_li.find('a', {'class': 'company_search_result'}).get('href')
    print(url)

    # Read the company's page 
    driver.get("https://opencorporates.com" + url)


    # Update soup
    soup = BeautifulSoup(driver.page_source, features="lxml")

    # Wait until the desired elements are present or visible on the page
    wait = WebDriverWait(driver, 20)  # Maximum wait time of 10 seconds
    company_number = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "company_number")))

    # Create a BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, features="lxml")

    # Print the text of the element
    # print(company_number.text)

    # Company Name
    company_name_obj = soup.find("h1", class_="wrapping_heading")
    company_name_string = "DEFAULT_VALUE"
    if company_name_obj is None:
        company_name_string = "N/A"   
    else:
        company_name_string = company_name_obj.text.strip()
    print("company_name: " + company_name_string)


    # Company Number
    company_number_obj = soup.find("dd", class_="company_number")
    company_number_string = "DEFAULT_VALUE"
    if company_number_obj is None:
        company_number_string = "N/A" 
    else:
        company_number_string = company_number_obj.text
    print("company_number: " + company_number_string)


    # Status
    status_obj = soup.find("dd", class_="status")
    status_string = "DEFAULT_VALUE"
    if status_obj is None:
        status_string = "N/A"
    else:
        status_string = status_obj.text.strip()
    print("status: " + status_string)


    # Incorporation Date
    incorporation_date_obj = soup.find("dd", class_="incorporation_date")
    incorporation_date_string = "DEFAULT_VALUE"
    if incorporation_date_obj is None:
        incorporation_date_string = "N/A"
    else:
        incorporation_date_string = incorporation_date_obj.text
    print("incorporation_date: " + incorporation_date_string)


    # Dissolution Date
    dissolution_date_obj = soup.find("dd", class_="dissolution date")
    dissolution_date_string = "DEFAULT_VALUE"
    if dissolution_date_obj is None: 
        dissolution_date_string = "N/A"
    else:
        dissolution_date_string = dissolution_date_obj.text
    print("dissolution_date: " + dissolution_date_string)


    # Company Type
    company_type_obj = soup.find("dd", class_="company_type")
    company_type_string = "DEFAULT_VALUE"
    if company_type_obj is None:
        company_type_string = "N/A"
    else:
        company_type_string = company_type_obj.text.strip()
    print("company_type: " + company_type_string)


    # Jurisdiction
    jurisdiction_obj = soup.find("dd", class_="jurisdiction")
    jurisdiction_string = "DEFAULT_VALUE"
    if jurisdiction_obj is None:
        jurisdiction_string = "N/A"
    else:
        jurisdiction_string = jurisdiction_obj.text.strip()
    print("jurisdiction: " + jurisdiction_string)


    # Business Number
    business_number_obj = soup.find("dd", class_="business_number")
    business_number_string = "DEFAULT_VALUE"
    if business_number_obj is None:
        business_number_string = "N/A"
    else:
        business_number_string = business_number_obj.text.strip()
    print("business_number: " + business_number_string)

    # Registry Page
    registry_page_obj = soup.find("dd", class_="registry_page")
    registry_page_string = "DEFAULT_VALUE"
    if registry_page_obj is None:
        registry_page_string = "N/A"
    else:
        registry_page_string = registry_page_obj.text.strip()
    print("registry_page: " + registry_page_string)


    print("--------------------FILINGS INFORMATION-------------------------")


    #################### For Storing Data as DataFrame in a Cell #####################
    # filing_header = [
    #     "Filing Name",
    #     "Filing URL",
    #     "Filing Date",
    #     "Filing Number"
    #     "Filing Type",
    #     "Filing Code"
    # ]
    # filing_df = pd.DataFrame(columns = filing_header)
    ###################################################################################


    list_of_filings = []
    filings = soup.find_all("a", class_="filing")
    for filing in filings:

        filing_name_string = filing.text
        filing_url_string = filing.get("href")
        print("filing_name: " + filing_name_string)
        print("filing_url: " + filing_url_string)
        filing_soup = get_filing_soup_from_url("https://opencorporates.com" + filing_url_string) # debug
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

        #################### For Storing Data as DataFrame in a Cell #####################
        # filing_dict = {}
        # filing_dict["Filing Name"] = filing_name_string
        # filing_dict["Filing URL"] = filing_url_string
        # filing_dict["Filing Date"] = filing_date_string
        # filing_dict["Filing Type"] = filing_type_string
        # filing_dict["Filing Code"] = filing_code_string
        # filing_df = filing_df.append(filing_dict, ignore_index=True)
        ############################################################

        
        ################### Storing Data As List of Tuples ###############################
        name_tuple = ("Filing Name", filing_name_string)
        url_tuple = ("Filing URL", filing_url_string)
        date_tuple = ("Filing Date", filing_date_string)
        type_tuple = ("Filing Type", filing_type_string)
        code_tuple = ("Filing Code", filing_code_string)

        filing_list = []
        filing_list.append(name_tuple)
        filing_list.append(url_tuple)
        filing_list.append(date_tuple)
        filing_list.append(type_tuple)
        filing_list.append(code_tuple)

        list_of_filings.append(filing_list)
        ###################################################################################

    print("--------------------------------------------------------------")


    # Source
    source_obj = soup.find("span", class_="publisher")
    source_string = "DEFAULT_VALUE"
    if source_obj is None:
        source_string = "N/A"
    else:
        source_string = source_obj.text.strip()
    print("source: " + source_string)


    ################################ Latest Events ################################

    # Option to store data in a list instead of a dataframe
    ################################################################################
    # list_of_events = [] 
    ################################################################################

    events = soup.find_all("div", class_="event-timeline-row")

    event_df_header = [
        "Event Date",
        "Event Description"
    ] 

    event_df = pd.DataFrame(columns = event_df_header)

    for event in events:
        event_dict = {}
        # event_list = []
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

        event_dict["Event Date"] = date_string
        event_dict["Event Description"] = description_string
        event_df = event_df.append(event_dict, ignore_index=True)

        
        # Option to store data in a list of tuples instead of a dataframe
        ################################################################################
        # date_tuple = ("Event Date", date_string)
        # description_tuple = ("Event Description", description_string)

        # event_list.append(date_tuple)
        # event_list.append(description_tuple)

        # list_of_events.append(event_list)
        ################################################################################



    data = {}
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
    # data['Recent Filings'] = filing_df
    data['Source'] = source_string
    data['Latest Events'] = event_df

    df = df.append(data, ignore_index=True)

    print(df)


print_loading("Saving scraped data in a CSV file")

df.to_csv('scraper_company_output.csv', index=False)

print("Done.")

# Quit the driver
driver.quit()
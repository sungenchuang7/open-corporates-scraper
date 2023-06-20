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
from selenium.webdriver.common.keys import Keys
import sys


def main():
    mode_selection = input("Type '1' to scrape company data or '2' to scrape officer data: ")
    if mode_selection.strip().lower() == "1": 
        print(1)
        exec(open('scraper_company.py').read())
    elif mode_selection.strip().lower() == "2":
        print(2)
        exec(open('scraper_officer.py').read())


if __name__ == "__main__":
    main()

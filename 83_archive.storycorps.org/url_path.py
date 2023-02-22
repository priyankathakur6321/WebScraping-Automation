from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import docx2txt
import pandas as pd
import textract
from selenium import webdriver
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
url = 'https://archive.storycorps.org/search/interviews/'
action = ActionChains(driver)
url_list = []
skip_list=[]
# base_dir = './dl.tufts.edu'
count=1
print(url)
# driver.maximize_window()

ird=2
try:
    driver.get(url)
    time.sleep(5)
    podcast=driver.find_element_by_xpath('//div[@class="container-fluid search-results-container"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        if link.startswith('https://archive.storycorps.org/interviews/'):
            print(link, 'episode')
            url_list.append(link)
    while ird!=401:
        print('next page>>',ird)
        driver.get('https://archive.storycorps.org/search/interviews/?search_type=basic&search_context=interviews&page_num='+str(ird)+'&page_size=25&sort_by=relevance&view_by=grid&visibility=all')
        time.sleep(5)
        podcast = driver.find_element_by_xpath('//div[@class="container-fluid search-results-container"]')
        a = podcast.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            if link.startswith('https://archive.storycorps.org/interviews/'):
                print(link, 'episode')
                url_list.append(link)
        ird+=1

except Exception as e:
    print(e)
    pass

data_list=set(url_list)
print(len(data_list), "final....#####")
df = pd.DataFrame(data_list)
df.to_csv('urls_data.csv')




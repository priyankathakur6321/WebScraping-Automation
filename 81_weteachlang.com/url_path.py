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
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://pearll.nflc.umd.edu/podcast/'
action = ActionChains(driver)
url_list = []
skip_list=[]
# base_dir = './dl.tufts.edu'
count=1
print(url)
# driver.maximize_window()
driver.get(url)
ird = 2
time.sleep(10)

try:
    podcast=driver.find_element_by_xpath('//div[@class="vc_pageable-slide-wrapper vc_clearfix"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        if link.startswith('https://pearll.nflc.umd.edu/'):
            print(link, 'episode')
            url_list.append(link)
except:
    pass

data_list=set(url_list)
print(len(data_list), "final....#####")
df = pd.DataFrame(data_list)
df.to_csv('urls_data.csv')
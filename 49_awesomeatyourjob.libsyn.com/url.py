import pandas as pd
import textract
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import docx2txt
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://awesomeatyourjob.libsyn.com/'
action = ActionChains(driver)
url_list = []
skip_list=[]
base_dir = './awesomeatyourjob.libsyn.com'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
print(url)
driver.get(url)
time.sleep(4)
idx=1
try:
    podcast=driver.find_element_by_xpath('//div[@class="libsyn-item-list"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link,'episode')
        url_list.append(link)
    time.sleep(3)
    while idx!=23:
        driver.find_element_by_xpath('//a[@class="nextPage"]').click()
        time.sleep(5)
        podcast = driver.find_element_by_xpath('//div[@class="libsyn-item-list"]')
        a = podcast.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            print(link,"episode")
            url_list.append(link)
        idx+=1
        time.sleep(2)
except:
    pass
url_list=list(set(url_list))
len_1 = len(url_list)
print(url_list)
df = pd.DataFrame(url_list)
df.to_csv('urls_data.csv')
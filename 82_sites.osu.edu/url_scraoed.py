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
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

# options = Options()
# options.headless = True
# driver = webdriver.Firefox()

url = 'https://www.capradio.org/programs/podcast'
# action = ActionChains(driver)
url_list = []
skip_list=[]
# base_dir = './dl.tufts.edu'
count=1
print(url)
# driver.maximize_window()
driver.get(url)

time.sleep(10)

try:
    element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "myDynamicElement")))
finally:
    driver.quit()


try:
    print('getting url')
    podcast=driver.find_element_by_xpath('//div[@class="podcast-block podfiltered"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        if link.startswith('https://www.capradio.org/'):
            print(link, 'episode')
            url_list.append(link)
    while True:
        driver.find_element_by_xpath('//p[@class="prev-button"]').click()
        time.sleep(4)
        podcast = driver.find_element_by_xpath('//section[@class="story-list"]')
        a = podcast.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            if link.startswith('https://www.capradio.org/'):
                print(link, 'episode')
                url_list.append(link)
except:
    pass

data_list=set(url_list)
print(len(data_list), "final....#####")
df = pd.DataFrame(data_list)
df.to_csv('urls_data.csv')
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import textract
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("testimonies_urls_data.csv")
url_list = list(set(url_path['0']))
len_1 = len(url_list)
base_dir = './wisconsinhistory.org'
count=1
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
for za in url_list:
    print("Opening Post url number:",str(count)+'/'+str(len_1))
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    try:
        print(za)
        driver.get(za)
        time.sleep(5)
        title_data = driver.find_element_by_xpath('//*[@id="subnav"]')
        title_data = title_data.text
        title, _ = title_data.split("\n", 1)
        print(title)
        Main_file_name=title.replace(" ", "_")
        file_name=Main_file_name
        transcript_link = driver.find_element_by_xpath('//*[@id="buttonlist"]')
        a = transcript_link.find_element_by_tag_name('a')
        transcript_url = a.get_attribute('href')
        print(transcript_url,'transcript_url')
        path = os.path.join(base_dir, Main_file_name)
        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
        t=1
        download_file(transcript_url, "transcript")
        time.sleep(2)

        text_trans = textract.process('transcript.pdf')
        print("text_trans",path,"title:",title)

        with open(Main_file_name + '_orig.txt', 'w') as f:
            f.write(text_trans)
        with open(Main_file_name + '.txt', 'w') as f:
                f.write(title)
        with open(Main_file_name + '_info.txt', 'w') as f:
            f.write(za + '\n'+transcript_url)
        print("Scraped transcript data")
        if os.path.exists('./transcript.pdf'):
            os.remove('./transcript.pdf')

        shutil.move(Main_file_name + '_orig.txt', path + '/' + Main_file_name + '_orig.txt')
        shutil.move(Main_file_name + '.txt', path + '/' + Main_file_name + '.txt')
        shutil.move(Main_file_name + '_info.txt', path + '/' + Main_file_name + '_info.txt')
        print("Done.")
        time.sleep(2)

    except:
        pass
    count+=1
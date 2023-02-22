

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
url = 'https://saas.transistor.fm/episodes'
action = ActionChains(driver)
url_list = []
base_dir = './saas.transistor.fm'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

print(url)
driver.get(url)
time.sleep(4)
ir=1
try:

    podcast=driver.find_element_by_xpath('//div[@class="site-episodes"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        if link.startswith('https://saas.transistor.fm'):
            url_list.append(link)
        else:
            pass
    time.sleep(3)
    while True:
        driver.find_element_by_xpath('//a[@class="page-item next-page"]').click()
        time.sleep(5)
        podcast = driver.find_element_by_xpath('//div[@class="site-episodes"]')
        a = podcast.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            print(link)
            if link.startswith('https://saas.transistor.fm'):
                url_list.append(link)
            else:
                pass


except:
    pass
url_list=list(set(url_list))
len_1 = len(url_list)
print(url_list)
for za in url_list:
    print(za)
    driver.get(za)
    print("Opening Post url number:", str(count) + '/' + str(len_1))
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    try:

        time.sleep(4)
        title1 = driver.find_element_by_xpath('//h2[@class="site-episode-title"]')
        title = title1.text
        print(title)

        date_ = driver.find_element_by_xpath('//span[@class="site-episode-metadata"]/time')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")

        driver.find_element_by_xpath('//a[@class="site-episode-transcript-link"]').click()
        time.sleep(3)
        transcript_link=driver.find_element_by_xpath('//div[@class="site-content-text site-episode-show-notes"]')
        transcript = transcript_link.text
        print(transcript)
        time.sleep(8)

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n","_")
        file_name = file_name.replace("/", "")
        time.sleep(4)

        try:
            audio_lnk=driver.find_element_by_xpath('//header[@class="site-episode-header"]/button[1]')
            audio_lnk=audio_lnk.get_attribute('data-url')
            print(audio_lnk,"audio_link")
            time.sleep(4)
            driver.get(audio_lnk)
            time.sleep(3)
            text = "audio_file"
            params = {
                "ie": "UTF-8",
                "client": "tw-ob",
                "q": text,
                "tl": "en",
                "total": "1",
                "idx": "0",
                "textlen": str(len(text))
            }
            # headers = {
            #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

            response = requests.get(audio_lnk, params=params)

            response.raise_for_status()
            print('download..')

            # assert response.headers["Content-Type"] == "audio/mpeg"
            with open("output.mp3", "wb") as file:
                file.write(response.content)
            print("Done.")

            os.rename("output.mp3", file_name + ".mp3")


            path = os.path.join(base_dir, file_name)
            os.mkdir(path)
            with open(file_name + '_orig.txt', 'w') as f:
                for line in transcript:
                    f.write(line)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(za + '\n')
                f.write(post_date)
            print("Scraped transcript data")

            shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
            print('audio moved successful')
            shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
            shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
            shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
            print("Done.")
            if os.path.exists('./transcript.pdf'):
                os.remove('./transcript.pdf')


        except Exception as e:
            print(e)
            pass
        count += 1
    except Exception as e:
        print("++++++++++++++++++")
        count += 1
        pass

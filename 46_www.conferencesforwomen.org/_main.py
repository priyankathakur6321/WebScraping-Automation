

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
url = 'https://www.conferencesforwomen.org/workload-overload-thats-a-good-question/'
action = ActionChains(driver)
url_list = []
base_dir = './conferencesforwomen.org'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

while True:
    print(url)
    driver.get(url)
    time.sleep(4)
    print("Opening Post url number:", str(count))
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    try:

        time.sleep(4)
        title1 = driver.find_element_by_xpath('//h1[@class="entry-title"]')
        title = title1.text
        print(title)

        date_ = driver.find_element_by_xpath('//time[@class="post_date post_icon mr-4"]')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")

        # transcript_link=driver.find_element_by_link_text('VIEW TRANSCRIPT')
        # transcript_link=transcript_link.get_attribute('href')
        # print(transcript_link)
        transcript = driver.find_element_by_xpath('//div[@class="post_content mt-4"]')
        transcript = transcript.text
        time.sleep(8)

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n","_")
        time.sleep(4)
        url = driver.find_element_by_xpath('//div[@class="pagination_link flex-fill mr-3"]/a')
        url = url.get_attribute('href')

        try:
            audio_link=driver.find_element_by_xpath('//*[@id="blubrryplayer-1"]')
            If_link=audio_link.get_attribute('src')
            print(If_link)
            driver.get(If_link)
            time.sleep(4)
            audio_lnk = driver.find_element_by_xpath('//div[@class="button-primary button-primary-download"]/a')
            audio_lnk = audio_lnk.get_attribute('href')
            time.sleep(4)

            print(audio_lnk, "audio_link")
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
            response = requests.get(audio_lnk, params=params)
            response.raise_for_status()
            print('download..')

            # assert response.headers["Content-Type"] == "audio/mpeg"
            with open("output.mp3", "wb") as file:
                file.write(response.content)
            print("Done.")

            os.rename("output.mp3", file_name + ".mp3")
            # driver.get(transcript_link)
            time.sleep(4)


            path = os.path.join(base_dir, file_name)
            os.mkdir(path)
            with open(file_name + '_orig.txt', 'w') as f:
                for line in transcript:
                    f.write(line)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(url + '\n')
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
        url=url
        print('next episode..........')

    except Exception as e:
        print("++++++++++++++++++")
        count += 1
        pass

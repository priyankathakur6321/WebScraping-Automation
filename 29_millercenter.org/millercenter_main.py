# https://millercenter.org/the-presidency/presidential-speeches/march-12-1933-fireside-chat-1-banking-crisis
import pandas as pd
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
url = 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1933-first-inaugural-address'
action = ActionChains(driver)
url_list = []

base_dir = './millercenter.org'
count=1

# def download_file(download_url, filename):
#     response = urllib.request.urlopen(download_url)
#     file = open(filename + ".docx", 'wb')
#     file.write(response.read())
#     file.close()

while True:
    url=url
    print(url)
    print("Opening Post url number:", str(count))
    try:
        driver.get(url)
        time.sleep(4)
        title1 = ''
        title = ''
        transcript = ''
        audio_path = ''
        audio = ''
        post_date = ''
        file_name = ''

        try:
            title1 = driver.find_element_by_xpath('//h2[@class="presidential-speeches--title"]')
            title = title1.text
            print(title)
        except:
            print('no title')
            pass
        try:
            driver.find_element_by_xpath('//div[@class="transcript-btn-inner"]').click()
            print('clicked')
            time.sleep(5)
            transcript = driver.find_element_by_xpath('//div[@class="expandable-text-container"]')
            transcript = transcript.text
            print(transcript)
            print("transcript scraped")
        except:
            print('no transcript.')
            pass
        # date_ = driver.find_element_by_xpath('//div[@class="presidential-speeches--sidebar"]/div/div/p[2]')
        # date_ = date_.text
        # print(date_)
        # from dateutil.parser import parse
        #
        # date_ = parse(date_, fuzzy=True)
        # print(date_, 'parse')
        # post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        # print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//*[@id="popup-trigger"]').click()
            time.sleep(2)
            audio_path = driver.find_element_by_xpath('//*[@id="download-popup"]/li/a')
            link = audio_path.get_attribute('href')
            print(link, "audio_link")
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
            response = requests.get(link, params=params)
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
                f.write(url + '\n')
            print("Scraped transcript data")

            shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
            print('audio moved successful')
            shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
            shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
            shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
            print("Done.")
        except Exception as e:
            print(e)
            pass
        time.sleep(5)
        next_url=driver.find_element_by_xpath('//div[@class="next"]/div/div/div/div/div/span/a')
        url = next_url.get_attribute('href')
        count += 1
    except Exception as e:
        print("++++++++++++++++++",e)
        time.sleep(5)
        next_url = driver.find_element_by_xpath('//div[@class="next"]/div/div/div/div/div/span/a')
        url = next_url.get_attribute('href')
        count += 1
        pass




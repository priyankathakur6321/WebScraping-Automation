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
url_path = pd.read_csv("urls_data.csv")
url_list = list(set(url_path['0']))
len_1 = len(url_list)
base_dir = './hilcoglobal.com'
count=1
for i in url_list:
    print("Opening Post url number:",str(count)+'/'+str(len_1))
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    text_trans=''
    try:
        print(i)
        driver.get(i)
        time.sleep(5)
        title1 = driver.find_element_by_xpath('//h1[@class="cs-margin-remove-vertical"]')
        title = title1.text
        print(title)
        transcript = driver.find_element_by_xpath('//ul[@class="nav nav-tabs cs-padding-remove-horizontal cs-margin-top"]/li[2]/a')
        trans_link = transcript.get_attribute('href')
        file_name = title.replace(" ", "_")
        time.sleep(10)

        path = os.path.join(base_dir, file_name)
        if os.path.isdir(path):
            print('already..')
            pass
            time.sleep(200)
        else:
            os.mkdir(path)
        try:
            try:
                audio=driver.find_element_by_xpath('//*[@id="podcast-description"]/iframe')
                audio_link=audio.get_attribute('src')
            except:
                audio=driver.find_element_by_xpath('//*[@id="podcast-description"]/p[1]/iframe')
                audio_link=audio.get_attribute('src')
        except:
            audio=driver.find_element_by_xpath('//*[@id="podcast-description"]/p[2]/iframe')
            audio_link=audio.get_attribute('src')
        try:
            driver.get(audio_link)
            time.sleep(4)
            audio_new=driver.find_element_by_xpath('//div[@class="mejs-mediaelement"]/audio')
            link_audio=audio_new.get_attribute('src')
            print(link_audio, "audio_link")
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
            response = requests.get(link_audio, params=params)
            response.raise_for_status()
            print('download..')

            # assert response.headers["Content-Type"] == "audio/mpeg"
            with open("output.mp3", "wb") as file:
                file.write(response.content)
            print("Done.")
        except Exception as e:
            print(e)
            pass
        os.rename("output.mp3", file_name + ".mp3")

        time.sleep(4)
        print(trans_link)
        driver.get(trans_link)
        time.sleep(4)
        driver.find_element_by_xpath('//ul[@class="nav nav-tabs cs-padding-remove-horizontal cs-margin-top"]/li[2]').click()
        time.sleep(5)
        transcript_data=driver.find_element_by_xpath('//*[@id="podcast-translation"]')
        transcript=transcript_data.text
        print(transcript)
        with open(file_name + '_orig.txt', 'w') as f:
            for line in transcript:
                f.write(line)
        with open(file_name + '.txt', 'w') as f:
            for line in title:
                f.write(line)
        with open(file_name + '_info.txt', 'w') as f:
            f.write(i + '\n')
            f.write("post_date Not available")
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
    count += 1
    time.sleep(100)
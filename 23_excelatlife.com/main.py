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
base_dir = './excelatlife.com'
count=1
for ir in url_list:
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
        print(ir)
        driver.get(ir)
        time.sleep(5)
        if ir.endswith('.mp3'):
            pass
        else:
            try:
                title1 = driver.find_element_by_xpath('//*[@id="risk"]/div[1]/h2')
                title = title1.text
                print(title)
            except:
                print('2nd title')
                title1 = driver.find_element_by_xpath('//*[@id="audio"]/h2')
                title = title1.text
                print(title)

            transcript = driver.find_element_by_xpath('//*[@id="page_content"]/div')
            transcript = transcript.text
            print(transcript)
            file_name = title.replace(" ", "_")
            file_name = file_name.replace("/", "_")
            time.sleep(10)
            # path = os.path.join(base_dir, file_name)
            # os.mkdir(path)
            try:
                    audio=driver.find_element_by_xpath('//*[@id="audioPopup"]/div[4]/a')
                    audio_link=audio.get_attribute('href')
                    print(audio_link)
            except:
               print("can't find audio link")
            try:
                print(audio_link, "audio_link")
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
                response = requests.get(audio_link, params=params)
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
            with open(file_name + '_orig.txt', 'w') as f:
                for line in transcript:
                    f.write(line)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(ir + '\n')
                f.write("post_date Not available")
            print("Scraped transcript data")
            path = os.path.join(base_dir, file_name)
            os.mkdir(path)
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
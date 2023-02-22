

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
url = 'http://designingyourself.net/blog/'
action = ActionChains(driver)
url_list = []
base_dir = './designingyourself.net'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

irt=1
while irt!=31:
    za=url+str(irt)
    print(za)
    driver.get(za)
    print("Opening Post url number:", str(count) + '/' + str(30))
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    irt+=1
    try:

        time.sleep(4)
        title1 = driver.find_element_by_xpath('//h1[@class="entry-title"]')
        title = title1.text
        print(title)
        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n", "_")
        file_name = file_name.replace("/", "")
        time.sleep(4)
        if os.path.exists(base_dir + '/' + file_name):
            pass
        else:

            date_ = driver.find_element_by_xpath('//div[@class="post"]/header/span[2]/span/a/time')
            date_ = date_.text
            from dateutil.parser import parse

            date_ = parse(date_, fuzzy=True)
            print(date_, 'parse')
            post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            print(post_date, "post_date")

            try:
                try:
                    transcript_link=driver.find_element_by_link_text('Full Transcript')
                    transcript_link= transcript_link.get_attribute('href')
                except:
                    transcript_link=driver.find_element_by_link_text('Full transcript')
                    transcript_link= transcript_link.get_attribute('href')
            except:
                transcript_link=driver.find_element_by_link_text('Full transcript of this episode')
                transcript_link= transcript_link.get_attribute('href')
            print(transcript_link)
            time.sleep(8)


            time.sleep(4)

            try:

                audio_lnk=driver.find_element_by_xpath('//div[@class="sqs-audio-embed"]')
                audio_lnk=audio_lnk.get_attribute('data-url')
                print(audio_lnk, "audio_link")
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
                time.sleep(3)
                driver.get(transcript_link)
                time.sleep(5)
                transcript=driver.find_element_by_xpath('//div[@class="main-content"]')
                transcript=transcript.text
                print(transcript)
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

    except Exception as e:
        print("++++++++++++++++++")
        pass
    count += 1

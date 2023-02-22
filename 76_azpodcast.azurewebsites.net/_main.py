

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
# url = 'https://smartgrid.gov/search/?p=1&i=podcasts&s=-published'
action = ActionChains(driver)
url_list = []
base_dir = './azpodcast.azurewebsites.net'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

url='https://azpodcast.azurewebsites.net/post/Episode-427-SONiC'

while True:
    print(url)
    driver.get(url)
    print("Opening Post url number:", str(count))
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    rt=1
    try:
        next_eps = driver.find_element_by_xpath('//a[@class="nav-prev"]')
        next_eps = next_eps.get_attribute('href')
        print('mkioo')

        time.sleep(10)
        title1 = driver.find_element_by_xpath('//a[@class="taggedlink"]')
        title = title1.text
        print(title)

        date_ = driver.find_element_by_xpath('//span[@class="pubDate"]')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")


        transcript_link=driver.find_element_by_xpath('//*[@id="post0"]/div[1]/p[5]/a')
        transcript_link = transcript_link.get_attribute('href')
        print(transcript_link,'aaaaa')

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n","_")
        file_name = file_name.replace("/", "")
        file_name = file_name.replace('"', '')
        time.sleep(4)





        try:
            # iframe=driver.find_element_by_xpath('//div[@class="post-body entry-content"]/iframe')
            # iframe=iframe.get_attribute('src')
            # driver.get(iframe)
            # time.sleep(4)
            audio_lnk=driver.find_element_by_xpath('//*[@id="post0"]/div[1]/p[4]/a')
            audio_lnk=audio_lnk.get_attribute('href')
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
            driver.get(transcript_link)
            time.sleep(4)
            transcript=driver.find_element_by_xpath('/html/body')
            transcript=transcript.text
            if transcript=="":
                pass
            else:
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
    except Exception as e:
        print("++++++++++++++++++")
        count += 1
        pass
    url = next_eps



# https://jobseekersradio.com/listen/
import re

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
url = 'https://kingdompreppers.org/all-videos'
action = ActionChains(driver)
url_list = []
base_dir = './kingdompreppers.org'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

print(url)
driver.get(url)
time.sleep(4)
try:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    podcast=driver.find_element_by_xpath('//div[@class="content page-content"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        url_list.append(link)

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

        # try:
        #     date_ = driver.find_element_by_xpath('//p[@class="hero-carousel__sub-title  hero-carousel__sub-title--color-blue"]')
        # except:
        #     date_ = driver.find_element_by_xpath('//p[@class="hero-carousel__sub-title  hero-carousel__sub-title--color-white"]')
        # date_ = date_.text
        # from dateutil.parser import parse
        #
        # date_ = parse(date_, fuzzy=True)
        # print(date_, 'parse')
        # post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        # print(post_date, "post_date")

        transcript_link=driver.find_element_by_xpath('//*[@id="view-transcript"]')
        transcript_link.click()
        time.sleep(8)

        title = za
        title = title.replace('https://kingdompreppers.org/videos-posts/','')
        title = title.replace('/','')
        print(title)
        transcript=driver.find_element_by_xpath('//div[@class="sqs-block-content"]')
        transcript=transcript.text

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n","_")
        time.sleep(4)
        try:
            audio_link=driver.find_element_by_xpath('//div[@class="sqs-video-wrapper video-none"]')
            link=audio_link.get_attribute('data-html')
            # link=link.get_attribute()
            print(link, "audio_link")
            link=re.search("(?P<url>https?://[^\s]+)", link).group("url")
            link=link.replace('"','')
            print(link)
            driver.get('https://en.savefrom.net/1-youtube-video-downloader-123/')
            time.sleep(4)
            input=driver.find_element_by_xpath('//div[@class="tarea-wrap"]/input')
            input.send_keys(link)
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="sf_submit"]').click()
            time.sleep(20)
            audio_li=driver.find_element_by_xpath('//a[@class="link link-download subname ga_track_events download-icon"]')
            audio_li=audio_li.get_attribute('href')
            print(audio_li)
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
            response = requests.get(audio_li, params=params)
            response.raise_for_status()
            print('download..')

            # assert response.headers["Content-Type"] == "audio/mpeg"
            with open("output.mp4", "wb") as file:
                file.write(response.content)
            print("Done.")

            os.rename("output.mp4", file_name + ".mp4")
            path = os.path.join(base_dir, file_name)
            os.mkdir(path)
            with open(file_name + '_orig.txt', 'wb') as f:
                for line in transcript:
                    f.write(line)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(za + '\n')
                # f.write(post_date)
            print("Scraped transcript data")

            shutil.move(file_name + ".mp4", path + "/" + file_name + ".mp4")
            print('audio moved successful')
            shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
            shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
            shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
            print("Done.")



        except Exception as e:

            print(e)
            pass
        count += 1

    except Exception as e:
        print("++++++++++++++++++")
        count += 1
        pass
driver.refresh()
time.sleep(10)

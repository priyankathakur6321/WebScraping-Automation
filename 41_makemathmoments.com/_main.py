import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import textract
import docx2txt
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://makemathmoments.com/episode'
action = ActionChains(driver)
url_list = []

base_dir = './makemathmoments.com'
count=1
driver.maximize_window()
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
iaw=15
while iaw!=184:
    url = 'https://makemathmoments.com/episode'
    url=url+str(iaw)
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
    transcript_link=''
    try:
        title1 = driver.find_element_by_xpath('//h1[@class="entry-title"]')
        title = title1.text
        print(title)
        try:
            driver.find_element_by_xpath('//h5[@class="et_pb_toggle_title"]').click()
            print('clicked')
            time.sleep(5)
            transcript = driver.find_element_by_xpath('//div[@class="et_pb_toggle_content clearfix"]')
            transcript = transcript.text
            print(transcript)
            print("transcript scraped")
        except Exception as e:
            print(e)
            transcript = driver.find_element_by_xpath('//div[@class="fbxt-content--inner"]')
            transcript = transcript.text
            print(transcript)
            print("transcript scraped part2")

        date_ = driver.find_element_by_xpath('//p[@class="et_pb_title_meta_container"]/span[1]')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n","_")
        time.sleep(4)

        try:
            audioiframe_path = driver.find_element_by_xpath('//*[@id="fusebox-player-DOWkG93LBr"]/div/div[2]/div/div[3]/div/div/a[1]')
            link = audioiframe_path.get_attribute('href')
            if link.endswith('.mp3'):
                time.sleep(3)
            else:
                print("not an audio link",link)
                pass

            print(link, "audio_link")
            driver.get(link)
            for i in range(60, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write("{:2d} seconds remaining.".format(i))
                sys.stdout.flush()
                time.sleep(1)
            filepath = '/home/webtunixi5/Downloads'
            filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
            print(filename)
            time.sleep(10)
            shutil.move(os.path.join('.', filename), 'output.mp3')
            print("done....")

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
                f.write(post_date)
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
    except Exception as e:
        print("++++++++++++++++++")
        count += 1
        pass
    iaw+=1


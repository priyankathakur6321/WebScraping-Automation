# https://convergehq.libsyn.com/

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
url = 'https://convergehq.libsyn.com/'
action = ActionChains(driver)
url_list = []
base_dir = './smallagencygrowth.com'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".docx", 'wb')
    file.write(response.read())
    file.close()

print(url)
driver.get(url)
time.sleep(4)
# podcast=driver.find_element_by_xpath('//div[@class="col-lg-12 col-md-12 item-container"]')
# a = podcast.find_elements_by_tag_name('a')
# for x in a:
#     link = x.get_attribute('href')
#     print(link)
#     url_list.append(link)
try:
    i=0
    while i!=100:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        i+=1
    podcast = driver.find_element_by_xpath('//div[@class="col-lg-12 col-md-12 item-container"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        url_list.append(link)
except:
    pass
url_list=list(set(url_list))
len_1 = len(url_list)
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
        time.sleep(15)
        title1 = driver.find_element_by_xpath('//h2[@class="section-heading"]')
        title = title1.text
        print(title)
        # driver.find_element_by_xpath('//*[@id="proi-transcript-wrap"]/div[1]').click()
        # time.sleep(5)
        transcript = driver.find_element_by_xpath('//div[@class="col-lg-12 col-md-12 col-sm-12 right-side"]')
        transcript = transcript.text
        print(transcript)
        print("transcript scraped")

        date_ = driver.find_element_by_xpath('//div[@class="col-lg-12 col-md-12 col-sm-12 right-side"]/p[1]')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        time.sleep(4)
        try:
            audio_path = driver.find_element_by_xpath('//div[@class="col-lg-12 col-md-12 item-container"]/div[1]/div[1]/iframe')
            audio_path = audio_path.get_attribute('src')
            print(audio_path, 'aaaaaa')
            driver.get(audio_path)
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="download-player"]').click()
            for i in range(20, 0, -1):
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
                f.write(za + '\n')
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



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
base_dir = './blog.bruggen.com'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

url='http://blog.bruggen.com/2022/05/conways-game-of-life-in-neo4j.html'

while True:
    print(url)
    driver.get(url)
    print("Opening Post url number:", str(count))
    title1 = ''
    title = ''
    base_xpath='//*[@id="container"]/table[3]/tbody/tr[2]/td/table/tbody/'
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    rt=1
    try:
        next_eps = driver.find_element_by_xpath('//*[@id="Blog1_blog-pager-older-link"]')
        next_eps = next_eps.get_attribute('href')
        print('mkioo')

        time.sleep(10)
        title1 = driver.find_element_by_xpath('//h3[@class="post-title entry-title"]')
        title = title1.text
        print(title)

        date_ = driver.find_element_by_xpath('//h2[@class="date-header"]/span')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")


        transcript_link=driver.find_element_by_xpath('//div[@class="post-body entry-content"]')
        transcript = transcript_link.text
        print(transcript)

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n","_")
        file_name = file_name.replace("/", "")
        file_name = file_name.replace('"', '')
        time.sleep(4)


        try:
            iframe=driver.find_element_by_xpath('//div[@class="post-body entry-content"]/iframe')
            iframe=iframe.get_attribute('src')
            driver.get(iframe)
            time.sleep(4)
            audio_lnk=driver.find_element_by_xpath('//a[@class="sc-button sc-button-download sc-button-small sc-button-icon"]')
            audio_lnk.click()
            time.sleep(4)
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
            # driver.get(transcript_link)
            # time.sleep(4)

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


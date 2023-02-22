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
url = 'https://digitalcommons.csumb.edu/digital-proximities_archive/'
action = ActionChains(driver)
url_list = []

base_dir = './digitalcommons.csumb.edu'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

print(url)
driver.get(url)
time.sleep(4)
podcast=driver.find_element_by_xpath('//*[@id="gallery_items"]')
a = podcast.find_elements_by_tag_name('a')
for x in a:
    link = x.get_attribute('href')
    print(link)
    url_list.append(link)

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
        title1 = driver.find_element_by_xpath('//*[@id="title"]/p/a')
        title = title1.text
        print(title)
        try:
            # driver.find_element_by_xpath('//span[@class="kt-blocks-accordion-title"]').click()
            # print('clicked')
            time.sleep(5)
            transcript = driver.find_element_by_xpath('//*[@id="alpha-pdf"]')
            transcript_link = transcript.get_attribute('href')
            print(transcript_link,'transcript_link')
            print("transcript scraped")
        except Exception as e:
            print(e)
            pass

        date_ = driver.find_element_by_xpath('//*[@id="publication_date"]/p')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        time.sleep(4)
        try:
            audio_path = driver.find_element_by_xpath('//*[@id="file-list"]/div[2]/p/a')
            link = audio_path.get_attribute('href')
            print(link, "audio_link")
            driver.get(link)
            for i in range(900, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write("{:2d} seconds remaining.".format(i))
                sys.stdout.flush()
                time.sleep(1)
            filepath = '/home/webtunixi5/Downloads'
            filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
            print(filename)
            time.sleep(10)
            shutil.move(os.path.join('.', filename), 'output.wav')
            print("done....")



            os.rename("output.wav", file_name + ".wav")
            path = os.path.join(base_dir, file_name)
            os.mkdir(path)
            download_file(transcript_link, "transcript")
            time.sleep(2)
            text_trans = textract.process('transcript.pdf')
            print(text_trans)

            with open(file_name + '_orig.txt', 'wb') as f:
                f.write(text_trans)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(za + '\n')
                f.write(post_date)
            print("Scraped transcript data")
            if os.path.exists('./transcript.pdf'):
                os.remove('./transcript.pdf')

            shutil.move(file_name + ".wav", path + "/" + file_name + ".wav")
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


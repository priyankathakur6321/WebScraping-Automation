

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
url = 'https://firetalk.teex.org/podcasts/'
action = ActionChains(driver)
url_list = []
base_dir = './firetalk.teex.org'
count=1

# def download_file(download_url, filename):
#     response = urllib.request.urlopen(download_url)
#     file = open(filename + ".pdf", 'wb')
#     file.write(response.read())
#     file.close()


print(url)
driver.get(url)
time.sleep(10)
ir=1
try:
    podcast=driver.find_element_by_xpath('//div[@class="entry-content"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        url_list.append(link)
        if link.startswith('https://firetalk.teex.org/'):
            url_list.append(link)
        else:
            pass
    time.sleep(3)
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

        time.sleep(5)
        title1 = driver.find_element_by_xpath('//h1[@class="entry-title"]')
        title = title1.text
        print(title)

        # date_ = driver.find_element_by_xpath('//div[@class="entry-meta entry-meta-layout"]/p')
        # date_ = date_.text
        # from dateutil.parser import parse
        #
        # date_ = parse(date_, fuzzy=True)
        # print(date_, 'parse')
        # post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        # print(post_date, "post_date")
        #
        # iframe=driver.find_element_by_xpath('//div[@class="iframe-responsive-16x9"]/iframe')
        # iframe=iframe.get_attribute('src')
        # driver.get(iframe)
        # time.sleep(5)

        transcript_link=driver.find_element_by_xpath('//div[@class="content-area"]/div/article/div[2]')
        transcript = transcript_link.text
        time.sleep(8)

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n","_")
        file_name = file_name.replace("/", "")
        time.sleep(4)


        try:
            iframe=driver.find_element_by_xpath('//div[@class="content-area"]/div/article/div[2]/figure/iframe')
            iframe=iframe.get_attribute('src')
            driver.get(iframe)
            time.sleep(4)
            audio_lnk=driver.find_element_by_xpath('//div[@class="col-auto pb-actions pr-2"]/a[2]')
            audio_lnk=audio_lnk.get_attribute('href')
            print(audio_lnk,"audio_link")
            time.sleep(4)
            driver.get(audio_lnk)
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
            # time.sleep(8)
            # transcript=driver.find_element_by_xpath('/html/body/pre')
            # transcript=transcript.text
            print(transcript)
            with open(file_name + '_orig.txt', 'w') as f:
                for line in transcript:
                    f.write(line)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(za + '\n')
                # f.write(post_date)
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
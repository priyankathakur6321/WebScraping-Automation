

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
url = 'https://www.craftofconsulting.com/podcasts/'
action = ActionChains(driver)
url_list = []
base_dir = './craftofconsulting.com'
count=1
#
# def download_file(download_url, filename):
#     response = urllib.request.urlopen(download_url)
#     file = open(filename + ".docx", 'wb')
#     file.write(response.read())
#     file.close()
indx=1
remain=[8,9,11,21,35,40,41,50,64,69,72,75,76,79,89,92,116,117,126,134,138,157,158,160]
for i in remain:
    url='https://www.craftofconsulting.com/podcasts/episode-'+str(i)
    print(url)
    url_list.append(url)
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
        time.sleep(5)
        title1 = driver.find_element_by_xpath('//h1[@class="font_0"]')
        title = title1.text
        print(title)
        translinkURL=driver.find_element_by_xpath('//*[@id="comp-krz5io64"]/a')
        translinkURL=translinkURL.get_attribute('href')
        time.sleep(5)
        print(translinkURL, 'clicked')


        date_ = driver.find_element_by_xpath('//*[@id="comp-krz4upsd"]/p')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        if os.path.exists(base_dir+'/'+file_name):
            print('file already exist')
            count+=1
            pass
        else:
            time.sleep(4)
            try:
                A_LINK=driver.find_element_by_xpath('//*[@id="comp-krz5i7i2"]/a')
                a_link=A_LINK.get_attribute('href')
                driver.get(a_link)
                print('entering audio link')
                time.sleep(3)
                try:

                    iframe_link=driver.find_element_by_xpath('//div[@class="col-lg-12 col-md-12 item-container"]/div[1]/div[1]/iframe')
                    iframe_link=iframe_link.get_attribute('src')
                    driver.get(iframe_link)
                    time.sleep(4)
                    driver.find_element_by_xpath('//*[@id="download-player"]').click()
                except Exception as e:
                    print(e,'Audio link:',a_link)
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
                driver.get(translinkURL)
                try:

                    transcript = driver.find_element_by_xpath('//div[@class="lightweight-accordion-body"]')
                except:
                    transcript = driver.find_element_by_xpath('//*[@id="comp-ks6ier0i1"]')
                transcript = transcript.text
                print(transcript)
                print("transcript scraped")

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
            except Exception as e:

                print(e)
                pass
            count += 1
    except Exception as e:
        print("++++++++++++++++++")
        count += 1
        pass

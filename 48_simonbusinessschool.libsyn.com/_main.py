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
url = 'https://simonbusinessschool.libsyn.com/'
action = ActionChains(driver)
url_list = []
base_dir = './simonbusinessschool.libsyn.com'
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
    podcast=driver.find_element_by_xpath('//div[@class="libsyn-item-list"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        url_list.append(link)
    time.sleep(3)
    driver.find_element_by_xpath('//a[@class="nextPage"]').click()
    time.sleep(5)
    podcast = driver.find_element_by_xpath('//div[@class="libsyn-item-list"]')
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
    try:
        if za.startswith('https://simonbusinessschool.libsyn.com'):
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
                title1 = driver.find_element_by_xpath('//div[@class="libsyn-item-title"]')
                title = title1.text
                print(title)

                date_ = driver.find_element_by_xpath('//div[@class="libsyn-item-release-date"]')
                date_ = date_.text
                from dateutil.parser import parse

                date_ = parse(date_, fuzzy=True)
                print(date_, 'parse')
                post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
                print(post_date, "post_date")
                time.sleep(3)

                transcript_link=driver.find_element_by_xpath('//div[@class="libsyn-item"]/div[3]')
                transcript_link = transcript_link.find_elements_by_tag_name('a')
                for x2 in transcript_link:
                    link = x2.get_attribute('href')
                    if link.endswith('.pdf'):
                        trans_link=link
                        print(link)
                    else:
                        pass

                file_name = title.replace(" ", "_")
                file_name = file_name.replace("\n","_")
                time.sleep(4)

                try:
                    audio_link=driver.find_element_by_xpath('//div[@class="libsyn-item-player"]/iframe')
                    If_link=audio_link.get_attribute('src')
                    print(If_link)
                    driver.get(If_link)
                    time.sleep(4)
                    audio_lnk = driver.find_element_by_xpath('//*[@id="download-player"]')
                    audio_lnk = audio_lnk.click()
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
                    # driver.get(transcript_link)
                    time.sleep(4)


                    path = os.path.join(base_dir, file_name)
                    os.mkdir(path)
                    download_file(trans_link, 'transcript')
                    time.sleep(4)
                    transcript = textract.process('transcript.pdf')
                    print(transcript)
                    with open(file_name + '_orig.txt', 'wb') as f:
                        f.write(transcript)
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
                count += 1
                url=url
                print('next episode..........')

            except Exception as e:
                print("++++++++++++++++++")
                count += 1
                pass
        else:
            print('Episode url not valid')
            count += 1
            pass
    except:
        pass
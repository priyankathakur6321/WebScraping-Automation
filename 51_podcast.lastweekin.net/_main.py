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
url = 'https://podcast.lastweekin.net/episodes'
action = ActionChains(driver)
url_list = []
skip_list=[]
base_dir = './podcast.lastweekin.net'
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
    podcast=driver.find_element_by_xpath('//section[@class="site-content"]/div')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link,'episode')
        url_list.append(link)
    time.sleep(3)
    while True:
        nextpage=driver.find_element_by_xpath('//a[@class="page-item next-page site-button"]')
        nextpage=nextpage.get_attribute('href')
        driver.get(nextpage)
        time.sleep(5)
        podcast = driver.find_element_by_xpath('//section[@class="site-content"]/div')
        a = podcast.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            print(link,"episode")
            url_list.append(link)
        time.sleep(2)
except:
    pass
url_list=list(set(url_list))
len_1 = len(url_list)
print(url_list)
for za in url_list:
    print(za,'llllllllllllllllllllll')
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
        title1 = driver.find_element_by_xpath('//div[@class="site-episode-intro"]/h2')
        title = title1.text
        print(title)

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n", "_")
        if os.path.exists(base_dir + '/' + file_name):
            pass
        else:

            date_ = driver.find_element_by_xpath('//div[@class="site-episode"]/time/span')
            date_ = date_.text
            from dateutil.parser import parse

            date_ = parse(date_, fuzzy=True)
            print(date_, 'parse')
            post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            print(post_date, "post_date")
            time.sleep(3)

            transcript_link=driver.find_element_by_xpath('//div[@class="site-episode-show-notes"]')
            transcript = transcript_link.text
            time.sleep(4)

            try:
                # audio_link=driver.find_element_by_xpath('//a[@class="libsyn-item-player"]/iframe')
                # If_link=audio_link.get_attribute('src')
                # print(If_link)
                # driver.get(If_link)
                # time.sleep(4)
                audio_lnk = driver.find_element_by_xpath('//a[@title="Download Episode"]')

                audio_lnk = audio_lnk.get_attribute('href')
                time.sleep(4)

                print(audio_lnk, "audio_link")
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
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

                response = requests.get(audio_lnk, params=params)

                response.raise_for_status()
                print('download..')
                with open("output.mp3", "wb") as file:
                    file.write(response.content)
                print("Done.")

                os.rename("output.mp3", file_name + ".mp3")
                # driver.get(transcript_link)
                time.sleep(4)


                path = os.path.join(base_dir, file_name)
                os.mkdir(path)

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
        count += 1
        url=url
        print('next episode..........')

    except Exception as e:
        print("++++++++++++++++++")
        count += 1
        pass




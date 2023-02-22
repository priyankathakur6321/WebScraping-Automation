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
main_url = 'https://recruitingdaily.com/podcast-episode/hrci-hr-in-arabic-speaking-countries-with-amy-dufrane/'
action = ActionChains(driver)
url_list = []
base_dir = './recruitingdaily.com'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

idx=1

while True:
    print(main_url)
    driver.get(main_url)
    time.sleep(4)
    print("Opening Post url number:", str(count) )
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    try:
        time.sleep(4)
        title1 = driver.find_element_by_xpath('//*[@id="post-top"]/div/div[1]/div[1]/h1')

        title = title1.text
        print(title)
        next_eps = driver.find_element_by_xpath('//div[@class="nav-previous"]/a')
        next_eps = next_eps.get_attribute('href')
        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n", "_")
        file_name = file_name.replace("/", "")
        time.sleep(4)
        if os.path.exists(base_dir + '/' + file_name):
            pass
        else:
            try:
                date_ = driver.find_element_by_xpath('//span[@class="meta meta-post"]')
            except:
                date_ = driver.find_element_by_xpath('//time[@class="updated"]')
            date_ = date_.text
            from dateutil.parser import parse

            date_ = parse(date_, fuzzy=True)
            print(date_, 'parse')
            post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            print(post_date, "post_date")
            time.sleep(3)
            transcript = driver.find_element_by_xpath('//div[@class="podcast-transcript"]')
            transcript = transcript.text
            print(transcript, "naaaaaa")

            with open(file_name + '_orig.txt', 'w') as f:
                for line in transcript:
                    f.write(line)
            try:
                try:
                    # driver.find_element_by_xpath('//svg[@class="icon icon-pp-play"]').click()
                    # time.sleep(3)
                    # print('clicked')
                    audio_lnk = driver.find_element_by_xpath('//audio[@class="pp-podcast-episode"]')
                    audio_lnk = audio_lnk.get_attribute('src')
                except:
                    print('no audio link found.')
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
                # driver.get(transcript_link)
                time.sleep(4)


                path = os.path.join(base_dir, file_name)
                os.mkdir(path)

                with open(file_name + '.txt', 'w') as f:
                    for line in title:
                        f.write(line)
                with open(file_name + '_info.txt', 'w') as f:
                    f.write(main_url + '\n')
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
    print('next...', next_eps)
    main_url = next_eps
    print('next episode..........')

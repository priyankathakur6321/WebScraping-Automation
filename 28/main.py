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

action = ActionChains(driver)
url_path = pd.read_csv("2bbs_com_urls_data.csv")
url_list = list(set(url_path['0']))
len_1 = len(url_list)
base_dir = './smallagencygrowth.com'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".docx", 'wb')
    file.write(response.read())
    file.close()
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
        title1 = driver.find_element_by_xpath('//h1[@data-content-field="title"]')
        title = title1.text
        print(title)
        transcript = driver.find_element_by_xpath('//div[@class="col sqs-col-12 span-12"]/div[2]')
        transcript = transcript.text
        print("transcript scraped")

        date_ = driver.find_element_by_xpath('//time[@class="Blog-meta-item Blog-meta-item--date"]')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        time.sleep(4)
        try:
            audio_path = driver.find_element_by_xpath('//div[@class="download"]/a')
            link = audio_path.get_attribute('href')
            print(link, "audio_link")
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
            response = requests.get(link, params=params)
            response.raise_for_status()
            print('download..')

            # assert response.headers["Content-Type"] == "audio/mpeg"
            with open("output.mp3", "wb") as file:
                file.write(response.content)
            print("Done.")



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
        try:
            print("++++++++++++++++++")
            print(za)
            driver.get(za)
            time.sleep(15)
            title1 = driver.find_element_by_xpath('//h1[@data-content-field="title"]')
            title = title1.text
            print(title)
            transcript = driver.find_element_by_xpath('//div[@class="col sqs-col-12 span-12"]/div[2]')
            transcript = transcript.text
            print("transcript scraped")

            date_ = driver.find_element_by_xpath('//time[@class="Blog-meta-item Blog-meta-item--date"]')
            date_ = date_.text
            from dateutil.parser import parse

            date_ = parse(date_, fuzzy=True)
            print(date_, 'parse')
            post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            print(post_date, "post_date")
            file_name = title.replace(" ", "_")
            time.sleep(4)
            try:
                audio_path = driver.find_element_by_xpath('//div[@class="download"]/a')
                link = audio_path.get_attribute('href')
                print(link, "audio_link")
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
                response = requests.get(link, params=params)
                response.raise_for_status()
                print('download..')

                # assert response.headers["Content-Type"] == "audio/mpeg"
                with open("output.mp3", "wb") as file:
                    file.write(response.content)
                print("Done.")

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
        except:
            pass

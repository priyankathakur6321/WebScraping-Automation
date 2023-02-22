import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import textract
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("urls_data.csv")
url_list = list(set(url_path['0']))
len_1 = len(url_list)
base_dir = './talktomamipapi.com'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
for ir in url_list:
    print("Opening Post url number:",str(count)+'/'+str(len_1))
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    text_trans=''
    try:
        print(ir)
        driver.get(ir)
        time.sleep(5)
        if ir.endswith('.mp3'):
            pass
        else:
            title1 = driver.find_element_by_xpath('//h1[@class="entry-title entry-title--large p-name preSlide slideIn"]')
            title = title1.text
            print(title)


            transcript_pdf = driver.find_element_by_xpath('//div[@class="sqs-layout sqs-grid-12 columns-12"]/div[2]/div[2]/div/div/div/a')
            transcript_pdf= transcript_pdf.get_attribute('href')
            print(transcript_pdf)
            file_name = title.replace(" ", "_")
            file_name = file_name.replace("/", "_")
            file_name = file_name.replace(",", "")
            time.sleep(10)
            # date_ = driver.find_element_by_xpath('//time[@class="entry-date published updated"]')
            # date_ = date_.text
            # from dateutil.parser import parse
            #
            # date_ = parse(date_, fuzzy=True)
            # print(date_, 'parse')
            # post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            # print(post_date, "post_date")
            try:
                    audio=driver.find_element_by_xpath('//div[@class="sqs-layout sqs-grid-12 columns-12"]/div[2]/div[3]/div/div/div/a')
                    audio_link=audio.get_attribute('href')
                    print(audio_link)
            except:
               print("can't find audio link")
            try:
                print(audio_link, "audio_link")
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
                response = requests.get(audio_link, params=params)
                response.raise_for_status()
                print('download..')

                # assert response.headers["Content-Type"] == "audio/mpeg"
                with open("output.mp3", "wb") as file:
                    file.write(response.content)
                print("Done.")
            except Exception as e:
                print(e)
                pass
            os.rename("output.mp3", file_name + ".mp3")
            path = os.path.join(base_dir, file_name)
            os.mkdir(path)
            download_file(transcript_pdf, "transcript")
            time.sleep(2)

            text = textract.process('transcript.pdf')
            print(text)
            time.sleep(4)
            with open(file_name + '_orig.txt', 'wb') as f:
                f.write(text)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(ir + '\n')
                f.write("post_date Not available")
                # f.write(post_date)

            if os.path.exists('./transcript.pdf'):
                os.remove('./transcript.pdf')
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
    time.sleep(100)
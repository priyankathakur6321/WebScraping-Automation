import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import textract
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("urls_data.csv")
url_list = list(set(url_path['0']))
len_1 = len(url_list)
base_dir = './disabilityvisibilityproject.com'
count=1
for i in url_list:
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
        print(i)
        driver.get(i)
        time.sleep(10)
        title1 = driver.find_element_by_xpath('//h1[@class="entry-title"]')
        title = title1.text
        print(title)
        transcript = driver.find_element_by_xpath('//div[@class="the-content"]')
        a = transcript.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')

            if link.endswith('.pdf'):
                transcript_pdf=link
                print('transcript link', transcript_pdf)
                pass
            else:
                pass
        date_ = driver.find_element_by_xpath('//time[@class="entry-date published updated"]')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        time.sleep(10)
        try:

            audio_path = driver.find_element_by_xpath('//section[@class="entry entry-single"]/p[1]/a[2]')
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
            download_file(transcript_pdf, "transcript")
            time.sleep(2)

            text_trans= textract.process('transcript.pdf')
            # print(text)

            with open(file_name + '_orig.txt', 'wb') as f:
                    f.write(text_trans)

            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(i + '\n')
                f.write(post_date)
            print("Scraped transcript data")

            if os.path.exists('./transcript.pdf'):
                os.remove('./transcript.pdf')

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

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import docx2txt
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("urls_data.csv")
url_list = list(set(url_path['0']))
base_dir = './revealnews.org'

for i in url_list:
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    try:
        print(i)
        driver.get(i)
        time.sleep(10)
        title1 = driver.find_element_by_xpath('//h1[@class="entry-title entry-title--with-subtitle"]')
        title1 = title1.text
        try:
            title2 = driver.find_element_by_xpath('//div[@class="newspack-post-subtitle"]')
            title = title1 + os.linesep + title2.text
        except:
            title = title1
        print(title)
        transcript = driver.find_element_by_xpath('//div[@class="entry-content"]')
        transcript = transcript.text
        date_ = driver.find_element_by_xpath('//time[@class="entry-date published"]')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")
        file_name = title1.replace(" ", "_")
        time.sleep(10)
        try:

            audio_path = driver.find_element_by_xpath('//figure[@class="wp-block-audio newspack-podcast-player"]/amp-audio/a')
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
                f.write(i + '\n')
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
    except Exception as e:
        print("++++++++++++++++++")
        pass


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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
import pandas as pd
import time
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
driver = webdriver.Chrome(ChromeDriverManager().install())

# driver = webdriver.Chrome('./chromedriver')
action = ActionChains(driver)
list_main = []
list_1 = []
url = 'https://www.usmle.org/podcasts'
base_dir = './usmle.org'
indx = 2

try:
    driver.get(url)
    time.sleep(4)
    while True:
        load_more = driver.find_element_by_xpath('//div[@class="c-iframe__embed"]')
        title=driver.find_element_by_class_name("c-iframe__title")
        title=title.text
        date_=title
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        print(file_name)

        transcript_link=driver.find_element_by_xpath('//span[@class="file file--mime-application-pdf file--application-pdf"]')
        transcript_link = transcript_link.find_element_by_tag_name('a')
        transcript_link=transcript_link.get_attribute('href')
        print("transcript_link",transcript_link)
        iframe_path = load_more.find_elements_by_tag_name('iframe')
        for x in iframe_path:
            link1 = x.get_attribute('src')
            print(link1)
            driver.get(link1)
            time.sleep(4)
            audio_path = driver.find_element_by_xpath('//div[@class="mejs-mediaelement"]')
            audio_path = audio_path.find_element_by_tag_name('audio')
            link =audio_path.get_attribute('src')
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

            download_file(transcript_link, "transcript")
            time.sleep(2)

            text_trans = textract.process('transcript.pdf')
            # print(text)

            with open(file_name + '_orig.txt', 'wb') as f:
                f.write(text_trans)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(transcript_link + '\n')
                f.write(link1 + '\n')
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




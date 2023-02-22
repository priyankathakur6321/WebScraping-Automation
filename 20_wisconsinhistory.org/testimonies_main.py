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
url_path = pd.read_csv("testimonies_urls_data.csv")
url_list = ['https://www.wisconsinhistory.org/HolocaustSurvivors/Peltz.asp','https://www.wisconsinhistory.org/HolocaustSurvivors/Applegate.asp']
len_1 = len(url_list)
base_dir = './wisconsinhistory.org'
count=1
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
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
        title_data = driver.find_element_by_xpath('//*[@id="subnav"]')
        title_data = title_data.text
        title1, _ = title_data.split("\n", 1)
        print(title1)
        Main_file_name=title1.replace(" ", "_")
        transcript_link = driver.find_element_by_xpath('//*[@id="buttonlist"]')
        a = transcript_link.find_element_by_tag_name('a')
        transcript_url = a.get_attribute('href')
        print(transcript_url,'transcript_url')
        xpath_base='//*[@id="audio-summary"]/'
        path = os.path.join(base_dir, Main_file_name)
        # os.mkdir(path)
        t=2
        while True:
            audio_xpath=xpath_base+'div['+str(t)+']'
            print(audio_xpath)
            data_link=driver.find_element_by_xpath(audio_xpath)
            title2=data_link.text
            title2, _ = title2.split("\n", 1)
            title =title1+title2
            print('full title',title,audio_xpath)
            time.sleep(4)
            audio_link = driver.find_element_by_xpath(audio_xpath+'/audio')
            audio_link=audio_link.get_attribute('src')
            print(audio_link)
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
                for i in range(10, 0, -1):
                    sys.stdout.write("\r")
                    sys.stdout.write("{:2d} seconds remaining.".format(i))
                    sys.stdout.flush()
                    time.sleep(1)
                response.raise_for_status()
                time.sleep(10)
                print('download..')
                with open("output.mp3", "wb") as file:
                    file.write(response.content)
                print("Done.")
                time.sleep(4)
            except Exception as e:
                print(e)
                pass
            file_name = title.replace(" ", "_")
            os.rename("output.mp3", file_name + ".mp3")
            shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
            print('audio moved successful')
            t+=1

        download_file(transcript_url, "transcript")
        time.sleep(2)

        text_trans = textract.process('transcript.pdf')
        # print(text)

        with open(file_name + '_orig.txt', 'wb') as f:
            f.write(text_trans)

        with open(Main_file_name + '.txt', 'w') as f:
            for line in title:
                f.write(line)
        with open(Main_file_name + '_info.txt', 'w') as f:
            f.write(za + '\n')
            f.write(trascript_link + '\n')
        print("Scraped transcript data")
        if os.path.exists('./transcript.pdf'):
            os.remove('./transcript.pdf')

        shutil.move(Main_file_name + '_orig.txt', path + '/' + Main_file_name + '_orig.txt')
        shutil.move(Main_file_name + '.txt', path + '/' + Main_file_name + '.txt')
        shutil.move(Main_file_name + '_info.txt', path + '/' + Main_file_name + '_info.txt')
        print("Done.")
        time.sleep(2)

    except:
        pass
    count+=1
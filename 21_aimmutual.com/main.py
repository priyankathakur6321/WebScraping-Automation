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
url_list = pd.read_csv("data_url.csv")
title_list=list(url_list['title'])
post_date_list=list(url_list['post_date'])
transcript_list=list(url_list['transcript_link'])
audio_list=list(url_list['audio_link'])
print(title_list)
base_dir='./aimmutual.com'
for i in range(len(title_list)):
    title=''
    transcript=''
    post_date=''
    transcript_url=''
    audio_link=''
    title=title_list[i]
    print(title)
    post_date=post_date_list[i]
    print(post_date)
    from dateutil.parser import parse

    post_date = parse(post_date, fuzzy=True)
    print(post_date, 'parse')
    post_date = datetime.strptime(str(post_date), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
    print(post_date, "post_date")
    file_name = title.replace(" ", "_")
    transcript_url = transcript_list[i]
    try:
        driver.get(transcript_url)
        transcript = driver.find_element_by_xpath('//div[@class="container pt-5 pb-5 "]')
        transcript= transcript.text
        print("transcript scraped")
    except Exception as e:
        print(e)
        pass
    audio_link=audio_list[i]
    try:
        print(audio_link,"audio")
        driver.get(audio_link)
        audio=driver.find_element_by_xpath('//div[@class="mejs-mediaelement"]/audio')
        audio=audio.get_attribute('src')
        print(audio, "audio_link")
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
        response = requests.get(audio, params=params)
        for i in range(10, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(i))
            sys.stdout.flush()
            time.sleep(1)
        response.raise_for_status()
        time.sleep(10)
        print('download..')

        # assert response.headers["Content-Type"] == "audio/mpeg"
        with open("output.mp3", "wb") as file:
            file.write(response.content)
        print("Done.")
        time.sleep(4)
        path = os.path.join(base_dir, file_name)
        os.mkdir(path)
    except Exception as e:
        print(e)
        pass
    os.rename("output.mp3", file_name + ".mp3")
    with open(file_name + '_orig.txt', 'w') as f:
        for line in transcript:
            f.write(line)
    with open(file_name + '.txt', 'w') as f:
        for line in title:
            f.write(line)
    with open(file_name + '_info.txt', 'w') as f:
        f.write(transcript_url + '\n')
        f.write(audio + '\n')
        f.write(post_date)
    print("Scraped transcript data")

    shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
    print('audio moved successful')
    shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
    shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
    shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
    print("Done.")
    time.sleep(150)




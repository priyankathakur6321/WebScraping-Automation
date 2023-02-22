import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import textract
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
base_dir='./ovcttac.gov'
action = ActionChains(driver)
url_path = pd.read_csv("urls_data.csv")
title_list = list(url_path['title'])
data_list = list(url_path['media_url'])
transcript_list = list(url_path['transcript_pdf'])
len_1 = len(title_list)
len_2 = len(data_list)
len_3 = len(transcript_list)
for i in range(len_1):
    title = ''
    transcript = ''
    audio = ''
    title=title_list[i]
    file_name = title.replace(" ", "_")
    try:
        data = data_list[i]
        print(data, "audio_link")
        text = "wmv_file"
        params = {
            "ie": "UTF-8",
            "client": "tw-ob",
            "q": text,
            "tl": "en",
            "total": "1",
            "idx": "0",
            "textlen": str(len(text))
        }
        response = requests.get(data,allow_redirects=True)
        for i in range(10, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(i))
            sys.stdout.flush()
            time.sleep(1)
        response.raise_for_status()
        time.sleep(5)
        print('download..')

        # assert response.headers["Content-Type"] == "audio/mpeg"
        with open("output.wmv", "wb") as file:
            file.write(response.content)
        os.rename("output.wmv", file_name + ".mp3")
        path = os.path.join(base_dir, file_name)
        os.mkdir(path)
        print("Done.")
    except:
        print("error in data")
        pass
    time.sleep(3)
    link_trans = transcript_list[i]
    download_file(link_trans, "transcript")
    time.sleep(2)
    text_trans = textract.process('transcript.pdf')
    with open(file_name + '_orig.txt', 'wb') as f:
            f.write(text_trans)
    with open(file_name + '.txt', 'w') as f:
        for line in title:
            f.write(line)
    with open(file_name + '_info.txt', 'w') as f:
        f.write(data + '\n')
        f.write(link_trans + '\n')
    print("Scraped transcript data")
    if os.path.exists('./transcript.pdf'):
        os.remove('./transcript.pdf')

    shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
    print('audio moved successful')
    shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
    shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
    shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
    print("Done.")

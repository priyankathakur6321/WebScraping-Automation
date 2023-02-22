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
url_path = pd.read_csv("urls_data.csv")
url_list = url_path.values.tolist()
len_1 = len(url_list)
base_dir = './braillists.org'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".docx", 'wb')
    file.write(response.read())
    file.close()

for ir in url_list:
    print("Opening Post url number:",str(count)+'/'+str(len_1))

    try:
        print(ir)

        title = ir[3]
        transcript_link = ir[2]

        audio_link = ir[1]
        print(title, audio_link)
        file_name = title.replace(" ", "_")
        file_name = file_name.replace("/", "_")
        file_name = file_name.replace(",", "")
        driver.get(transcript_link)
        time.sleep(10)
        print('transcript file downloaded..')
        filepath = '/home/webtunixi5/Downloads'
        filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
        print(filename)
        time.sleep(10)
        shutil.move(os.path.join('.', filename), 'transcript.docx')
        transcript = docx2txt.process("transcript.docx")
        with open(file_name + '_orig.txt', 'w') as f:
                f.write(transcript)
        print("transcript...")
        time.sleep(5)
        if os.path.exists('./transcript.docx'):
            os.remove('./transcript.docx')
        try:
            print(audio_link, "audio_link")
            response = requests.get(audio_link)
            response.raise_for_status()
            time.sleep(5)
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

        time.sleep(4)
        with open(file_name + '.txt', 'w') as f:
            for line in title:
                f.write(line)
        with open(file_name + '_info.txt', 'w') as f:
            f.write(audio_link + '\n')
            f.write(transcript_link)


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
    time.sleep(2)
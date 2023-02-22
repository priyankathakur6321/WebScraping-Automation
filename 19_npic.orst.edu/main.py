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

# driver = webdriver.Chrome('./chromedriver')
action = ActionChains(driver)
list_main = []
list_1 = []
base_dir = './npic.orst.edu'
url = 'http://npic.orst.edu/pestibytes/'
indx = 2

try:
    t = 1
    while True:
        driver.get(url)
        print(url)
        time.sleep(4)
        base_xpath = '//*[@id="pageDiv"]/table/tbody/'
        xpath = base_xpath + 'tr[' + str(t) + ']'
        print(xpath)
        data=driver.find_element_by_xpath(xpath+'/td[2]')
        title = ''
        title = data.text
        title1,title2 = title.split("-",1)
        print(title1)
        title=title1
        a = data.find_elements_by_tag_name('a')
        count = 1
        for x in a:
            link = x.get_attribute('href')
            if link.endswith('.mp3'):
                audio=link
            elif link.endswith('.html'):
                trascript_link=link
            else:
                pass
        try:
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
            try:

                driver.get(trascript_link)
                trans=driver.find_element_by_xpath('//*[@id="pageDiv"]')
                transcript=trans.text
                date_=driver.find_element_by_xpath('//*[@id="lastUpdated"]')
                date_ = date_.text
            except:
                print("not fonud transcript or post date")
                pass

            date_ = parse(date_, fuzzy=True)
            print(date_, 'parse')
            post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            print(post_date, "post_date")
            file_name = title.replace(" ", "_")
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
                f.write(url + '\n')
                f.write(trascript_link + '\n')
                f.write(post_date)
            print("Scraped transcript data")

            shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
            print('audio moved successful')
            shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
            shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
            shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
            print("Done.")
            time.sleep(150)

        except Exception as e:
            print(e)
            pass
        t += 1
except Exception as e:
        print(e)
        pass




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
url = 'https://www.wisconsinhistory.org/HolocaustSurvivors/testimonies.asp'
# url = 'https://www.wisconsinhistory.org/HolocaustSurvivors/excerpts/003756.asp'
url_list=[]
# try:
#     driver.get(url)
#     time.sleep(4)
#     count=1
#     while count!=89:
#         url=driver.find_element_by_xpath('//span[@class="NextPage"]/a')
#         url=url.get_attribute('href')
#         url_list.append(url)
#         print(url)
#         time.sleep(2)
#         driver.find_element_by_xpath('//span[@class="NextPage"]').click()
#         count+=1
#
# except Exception as e:
#     print(e)
#     pass
# print(len(url_list))
# list_main=set(url_list)
# print(len(list_main),"final....#####")
# df = pd.DataFrame(list_main)
# df.to_csv('urls_data.csv')
url_path = pd.read_csv("urls_data.csv")
url_list = list(set(url_path['0']))
len_1 = len(url_list)
base_dir = './wisconsinhistory.org'
count=1
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
for s_url in url_list:
    try:
        print(s_url)
        driver.get(s_url)
        time.sleep(3)
        title=driver.find_element_by_xpath('//*[@id="individual-entry-heading"]')
        title=title.text
        # title,_=title.split("|",1)
        print(title)
        file_name = title.replace(" ", "_")
        time.sleep(4)
        try:
            audio_link = driver.find_element_by_xpath('//*[@id="survivors-main"]/div[2]/audio')
            audio_link = audio_link.get_attribute('src')
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
            path = os.path.join(base_dir, file_name)
            os.mkdir(path)
            print(path)

            try:
                transcript_link = driver.find_element_by_xpath('//p[@class="excerpt-end"]')
                a = transcript_link.find_element_by_tag_name('a')
                transcript_url = a.get_attribute('href')
            except Exception as e:
                print(e)
            print(transcript_url, 'transcript_url')
            download_file(transcript_url, "transcript")
            time.sleep(2)

            text_trans = textract.process('transcript.pdf')
            # print(text)

            with open(file_name + '_orig.txt', 'wb') as f:
                f.write(text_trans)
            os.rename("output.mp3", file_name + ".mp3")
            print('audio moved successful')
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(s_url + '\n')
            print("Scraped transcript data")
            if os.path.exists('./transcript.pdf'):
                os.remove('./transcript.pdf')
            shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
            shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
            shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
            shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
            print("Done.")
            time.sleep(5)
        except:
            print("No match type")
            pass
    except Exception as e:
        print(e)
        pass


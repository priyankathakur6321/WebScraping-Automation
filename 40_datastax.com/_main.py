import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import textract
import docx2txt
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://www.datastax.com/resources/podcast/open-source-data'
action = ActionChains(driver)
url_list = []

base_dir = './datastax.com'
count=1
# driver.maximize_window()
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

print(url)
driver.get(url)
time.sleep(4)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
iuu=1
podcast = driver.find_element_by_xpath('//div[@class="available-episodes container"]')
a = podcast.find_elements_by_tag_name('a')
for x in a:
    link = x.get_attribute('href')
    print(link)
    url_list.append(link)
while iuu!=10:
    print(iuu)
    try:
        time.sleep(3)
        element=driver.find_element_by_xpath('//*[@id="__next"]/main/div[2]/div[2]/nav/ul/li['+str(iuu)+']')

        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        actions.click().perform()
        time.sleep(3)
        podcast = driver.find_element_by_xpath('//div[@class="available-episodes container"]')
        a = podcast.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            print(link)
            url_list.append(link)
    except Exception as e:
        print(e)
        pass
    iuu+=1


url_list=list(set(url_list))
len_1 = len(url_list)
for za in url_list:
    print("Opening Post url number:",str(count)+'/'+str(len_1))
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    transcript_link=''
    try:
        print(za)
        driver.get(za)
        time.sleep(15)
        title1 = driver.find_element_by_xpath('//div[@class="col-lg-8 col-12 offset-lg-2"]/h2')
        title = title1.text
        print(title)
        try:
            # driver.find_element_by_xpath('//span[@class="kt-blocks-accordion-title"]').click()
            # print('clicked')
            time.sleep(5)
            transcript = driver.find_element_by_xpath('//*[@id="podcast-transcript-content"]/span/p[1]/a')
            transcript_link = transcript.get_attribute('href')
            print(transcript_link,'transcript_link')
            print("transcript scraped")
        except Exception as e:
            print(e)
            transcript = driver.find_element_by_xpath('//*[@id="podcast-transcript-content"]')
            transcript = transcript.text
            print(transcript)
            print("transcript scraped")

        # date_ = driver.find_element_by_xpath('//*[@id="publication_date"]/p')
        # date_ = date_.text
        # from dateutil.parser import parse
        #
        # date_ = parse(date_, fuzzy=True)
        # print(date_, 'parse')
        # post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        # print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n","_")
        time.sleep(4)

        try:
            try:
                audio_path = driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/audio')
                link = audio_path.get_attribute('src')
            except:
                audioiframe_path = driver.find_element_by_xpath('//div[@class="player-container"]/div/span/p/iframe')
                audioiframe_path = audioiframe_path.get_attribute('src')
                driver.get(audioiframe_path)
                time.sleep(3)
                try:

                    link=driver.find_element_by_xpath('//a[@class="omny-btn download"]')
                    link=link.get_attribute('href')
                except:
                    link = driver.find_element_by_xpath('//div[@class="main-wrap size-normal"]/audio')
                    link = link.get_attribute('src')


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
            if transcript_link!="":
                download_file(transcript_link, "transcript")
                time.sleep(2)
                transcript = textract.process('transcript.pdf')
                print(transcript)
                with open(file_name + '_orig.txt', 'wb') as f:
                    f.write(transcript)
            else:
                with open(file_name + '_orig.txt', 'w') as f:
                    f.write(transcript)

            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(za + '\n')
                # f.write(post_date)
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


from io import BytesIO
from urllib.request import urlopen
import pandas as pd

import textract
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://www.rehab.research.va.gov/podcast/index.html'
action = ActionChains(driver)
url_list = []
base_dir = './rehab.research.va.gov'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()


print(url)
driver.get(url)
time.sleep(3)
ir=1
try:
    podcast=driver.find_element_by_xpath('//*[@id="JRRD_ArticleContent"]/div[3]/table/tbody')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        url_list.append(link)
        if link.startswith('https://www.rehab.research.va.gov/'):
            url_list.append(link)
        else:
            pass
    time.sleep(3)
except:
    pass
url_list=list(set(url_list))
len_1 = len(url_list)
print(url_list)
for za in url_list:
    print(za)
    if za.startswith('https://www.rehab.research.va.gov/'):
        driver.get(za)
        print("Opening Post url number:", str(count) + '/' + str(len_1))
        title1 = ''
        title = ''
        transcript = ''
        audio_path = ''
        audio = ''
        post_date = ''
        file_name = ''
        try:

            time.sleep(5)
            title1 = driver.find_element_by_xpath('//div[@align="center"]/table/tbody/tr[2]/td[2]/p')
            title1 = title1.text
            title=title1.split("\n")
            title=title[0]
            title = title.split(",")
            title = title[0]
            print(title)

            file_name = title.replace(" ", "_")
            file_name = file_name.replace("\n", "_")
            file_name = file_name.replace("/", "")
            time.sleep(4)
            if os.path.exists(base_dir + '/' + file_name):
                pass
            else:

                # date_ = driver.find_element_by_xpath('//div[@class="entry-meta entry-meta-layout"]/p')
                # date_ = date_.text
                # from dateutil.parser import parse
                #
                # date_ = parse(date_, fuzzy=True)
                # print(date_, 'parse')
                # post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
                # print(post_date, "post_date")

                # iframe=driver.find_element_by_xpath('//div[@class="iframe-responsive-16x9"]/iframe')
                # iframe=iframe.get_attribute('src')
                # driver.get(iframe)
                # time.sleep(5)

                try:
                    transcript_link=driver.find_element_by_link_text('[Text Transcript]')
                except:
                    print('transcript link not found')
                    pass
                transcript_link = transcript_link.get_attribute('href')
                print(transcript_link,'transcript link')
                time.sleep(8)

                # file_name = title.replace(" ", "_")
                # file_name = file_name.replace("\n","_")
                # file_name = file_name.replace("/", "")
                # time.sleep(4)


                try:
                    audio_lnk=driver.find_element_by_xpath('//*[@id="JRRD_ArticleContent"]/div[2]/table/tbody/tr[2]/td[2]/p/span/a[1]')
                    audio_lnk=audio_lnk.get_attribute('href')
                    print(audio_lnk,"audio_link")
                    time.sleep(4)
                    driver.get(audio_lnk)
                    time.sleep(3)
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
                    # headers = {
                    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

                    response = requests.get(audio_lnk, params=params)

                    response.raise_for_status()
                    print('download..')

                    # assert response.headers["Content-Type"] == "audio/mpeg"
                    with open("output.mp3", "wb") as file:
                        file.write(response.content)
                    print("Done.")

                    os.rename("output.mp3", file_name + ".mp3")


                    path = os.path.join(base_dir, file_name)
                    os.mkdir(path)
                    if transcript_link.endswith('.doc'):
                        driver.get(transcript_link)
                        time.sleep(10)

                        filepath = '/home/webtunixi5/Downloads'
                        filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
                        print(filename)
                        time.sleep(10)
                        shutil.move(os.path.join('.', filename), 'transcript.doc')
                        time.sleep(5)
                        os.rename("transcript.doc", file_name + ".doc")
                        shutil.move(file_name + '.doc', path + '/' + file_name + '_orig.doc')
                        # transcript = textract.process("transcript.doc")
                        # transcript = transcript.decode("utf-8")
                        # print(transcript)
                        # time.sleep(5)
                        # if os.path.exists('./transcript.doc'):
                        #     os.remove('./transcript.doc')

                    else:
                        download_file(transcript_link, "transcript")
                        time.sleep(2)
                        transcript = textract.process('transcript.pdf')
                        print(transcript)
                        with open(file_name + '_orig.txt', 'w') as f:
                            for line in transcript:
                                f.write(str(line))
                        shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')


                    with open(file_name + '.txt', 'w') as f:
                        for line in title:
                            f.write(line)
                    with open(file_name + '_info.txt', 'w') as f:
                        f.write(za + '\n')
                        # f.write(post_date)
                    print("Scraped transcript data")

                    shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
                    print('audio moved successful')
                    shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
                    shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
                    print("Done.")
                    if os.path.exists('./transcript.pdf'):
                        os.remove('./transcript.pdf')


                except Exception as e:
                    print(e)
                    pass

        except Exception as e:
            print("++++++++++++++++++")
            pass
    else:
        pass
    count += 1

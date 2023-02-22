

import pandas as pd
import textract
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
url = 'https://guides.statelibrary.sc.gov/podcasting/bibliobservatory'
action = ActionChains(driver)
url_list = []
base_dir = './guides.statelibrary.sc.gov'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".docx", 'wb')
    file.write(response.read())
    file.close()


print(url)
driver.get(url)
time.sleep(3)
ir=1
try:
    podcast=driver.find_element_by_xpath('//*[@id="s-lg-link-list-63344082"]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        if link.startswith('https://libraryvoices.podbean.com/'):
            url_list.append(link)
    time.sleep(3)


except:
    pass
url_list=list(set(url_list))
len_1 = len(url_list)
print(url_list)
for za in url_list:
    print(za)
    if za==None:
        pass
    else:
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
            title1 = driver.find_element_by_xpath('//div[@class="info"]/h2/a')
            title = title1.text

            print(title)

            date_ = driver.find_element_by_xpath('//div[@class="date"]')
            date_ = date_.text
            from dateutil.parser import parse

            date_ = parse(date_, fuzzy=True)
            print(date_, 'parse')
            post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            print(post_date, "post_date")

            # linkAA=driver.find_element_by_xpath('//div[@class="entry"]')
            # linkAA = linkAA.find_elements_by_tag_name('a')
            # for cd in linkAA:
            #     links = cd.get_attribute('href')
            #     if links.startswith('https://www.purpleorange.org.au'):
            #         transcript_link=links
            #     else:
            #         pass
            # print(transcript_link,'transcript link')
            # time.sleep(8)

            trans_eps=title.split('-')
            print(trans_eps)



            file_name = title.replace(" ", "_")
            file_name = file_name.replace("\n","_")
            file_name = file_name.replace("/", "")
            time.sleep(4)

            # driver.get('https://guides.statelibrary.sc.gov/podcasting/bibliobservatory')
            # time.sleep(4)
            transcript=" "
            # try:
            #     transcript_ll=driver.find_element_by_link_text('Download a transcript of the podcast here.')
            #     transcript_ll=transcript_ll.get_attribute('href')
            #     download_file(transcript_ll, "transcript")
            #     time.sleep(2)
            #     transcript = textract.process('transcript.docx')
            #     print(transcript)
            # except:
            #     transcript=driver.find_element_by_xpath('//*[@id="main"]')
            #     transcript=transcript.text
            #     print(transcript)



            try:
                iframe=driver.find_element_by_xpath('//a[@class="post_toolbar_download"]')
                iframe=iframe.get_attribute('href')
                driver.get(iframe)
                time.sleep(4)
                audio_lnk=driver.find_element_by_xpath('//a[@class="btn btn-ios download-btn"]')
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

                # driver.get(transcript_link)


                path = os.path.join(base_dir, file_name)
                os.mkdir(path)


                with open(file_name + '_orig.txt', 'w') as f:
                    for line in transcript:
                        f.write(str(line))
                with open(file_name + '.txt', 'w') as f:
                    for line in title:
                        f.write(line)
                with open(file_name + '_info.txt', 'w') as f:
                    f.write(za + '\n')
                    f.write(post_date)
                print("Scraped transcript data")

                shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
                print('audio moved successful')
                shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
                shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
                shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
                print("Done.")
                if os.path.exists('./transcript.docx'):
                    os.remove('./transcript.docx')


            except Exception as e:
                print(e)
                pass
            count += 1
        except Exception as e:
            print("++++++++++++++++++")
            count += 1
            pass


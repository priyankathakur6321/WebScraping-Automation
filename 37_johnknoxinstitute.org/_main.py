
# https://jobseekersradio.com/listen/


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
url = 'https://johnknoxinstitute.org/courses'
action = ActionChains(driver)
url_list = []
base_dir = './johnknoxinstitute.org'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

print(url)
driver.get(url)
time.sleep(4)
try:
    podcast=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]')
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        url_list.append(link)

except:
    pass
url_list=list(set(url_list))
len_1 = len(url_list)
print(url_list)
for za in url_list:
    print(za)
    driver.get(za)
    print("Opening Post url number:", str(count) + '/' + str(len_1))
    r=1
    while r!=50:
        try:
            try:
                ep_path='//*[@id="lessontable"]/tr['+str(r)+']/td[1]/a'
                driver.find_element_by_xpath(ep_path).click()
                print('chapter->',r)
            except:
                ep_path = '//*[@id="lessontable"]/tbody/tr[' + str(r) + ']/td[1]/a'
                driver.find_element_by_xpath(ep_path).click()
                print('chapter->', r)
        except:
            pass
        print(r)
        r+=1
        title1 = ''
        title = ''
        transcript = ''
        audio_path = ''
        audio = ''
        post_date = ''
        file_name = ''
        try:

            time.sleep(4)
            title1 = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div')
            title = title1.text
            print(title)
            # try:
            #     date_ = driver.find_element_by_xpath('//p[@class="hero-carousel__sub-title  hero-carousel__sub-title--color-blue"]')
            # except:
            #     date_ = driver.find_element_by_xpath('//p[@class="hero-carousel__sub-title  hero-carousel__sub-title--color-white"]')
            # date_ = date_.text
            # from dateutil.parser import parse
            #
            # date_ = parse(date_, fuzzy=True)
            # print(date_, 'parse')
            # post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            # print(post_date, "post_date")

            transcript_link=driver.find_element_by_xpath('//*[@id="downloadbuttons"]/a[5]')
            transcript_link=transcript_link.get_attribute('href')
            print(transcript_link)
            time.sleep(8)



            file_name = title.replace(" ", "_")
            file_name = file_name.replace("\n","_")
            time.sleep(4)
            try:
                audio_link=driver.find_element_by_xpath('//*[@id="downloadbuttons"]/a[4]')
                link=audio_link.get_attribute('href')
                print(link, "audio_link")
                driver.get(link)
                for i in range(80, 0, -1):
                    sys.stdout.write("\r")
                    sys.stdout.write("{:2d} seconds remaining.".format(i))
                    sys.stdout.flush()
                    time.sleep(1)
                filepath = '/home/webtunixi5/Downloads'
                filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
                print(filename)
                time.sleep(10)
                shutil.move(os.path.join('.', filename), 'output.mp3')
                print("done....")


                os.rename("output.mp3", file_name + ".mp3")

                driver.get(transcript_link)
                for i in range(10, 0, -1):
                    sys.stdout.write("\r")
                    sys.stdout.write("{:2d} seconds remaining.".format(i))
                    sys.stdout.flush()
                    time.sleep(1)
                filepath = '/home/webtunixi5/Downloads'
                filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
                print(filename)
                time.sleep(10)
                shutil.move(os.path.join('.', filename), 'transcript.pdf')
                print("done....")
                text_trans = textract.process('transcript.pdf')
                print(text_trans, "transcript scraped")
                path = os.path.join(base_dir, file_name)
                os.mkdir(path)
                with open(file_name + '_orig.txt', 'wb') as f:
                    f.write(text_trans)
                with open(file_name + '.txt', 'w') as f:
                    for line in title:
                        f.write(line)
                with open(file_name + '_info.txt', 'w') as f:
                    f.write(za + '\n')
                    # f.write(post_date)
                print("Scraped transcript data")

                shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
                print('audio moved successful')
                shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
                shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
                shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
                print("Done.")
                if os.path.exists('./transcript.pdf'):
                    os.remove('./transcript.pdf')


            except Exception as e:

                print(e)
                pass
            count += 1
        except Exception as e:
            print("++++++++++++++++++")
            count += 1
            pass

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
action = ActionChains(driver)
url_list = []
skip_list=[]
base_dir = './dl.tufts.edu'
count=1
# driver.maximize_window()
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

action = ActionChains(driver)
url_path = pd.read_csv("urls_data.csv")
url_list = list(url_path['0'])
len_1 = len(url_list)
len_1 = len(url_list)
print(url_list)
for za in url_list:
    print(za,'llllllllllllllllllllll')
    driver.get(za)
    time.sleep(5)
    print("Opening Post url number:", str(count) + '/' + str(len_1))
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    try:

        time.sleep(4)
        title1 = driver.find_element_by_xpath('//div[@class="col-xs-12 main-header"]/h2')
        title = title1.text
        print(title)

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n", "_")
        if os.path.exists(base_dir + '/' + file_name):
            pass
        else:

            date_ = driver.find_element_by_xpath('//div[@class="col-xs-12 main-header"]/p[2]')
            date_ = date_.text
            from dateutil.parser import parse

            date_ = parse(date_, fuzzy=True)
            print(date_, 'parse')
            post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            print(post_date, "post_date")
            time.sleep(3)

            driver.find_element_by_link_text('Transcript').click()
            time.sleep(3)
            transcript_link=driver.find_element_by_xpath('//div[@class="transcript_table"]')
            transcript = transcript_link.text
            time.sleep(4)

            try:
                audio_lnk = driver.find_element_by_link_text('Download Audio File')
                audio_lnk = audio_lnk.get_attribute('href')
                print(audio_lnk,"audio")
                time.sleep(4)
                driver.get(audio_lnk)
                time.sleep(4)
                for i in range(100, 0, -1):
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
                # driver.get(transcript_link)
                time.sleep(4)


                path = os.path.join(base_dir, file_name)
                os.mkdir(path)

                print(transcript)
                with open(file_name + '_orig.txt', 'w') as f:
                    for line in transcript:
                        f.write(line)
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
                if os.path.exists('./transcript.pdf'):
                    os.remove('./transcript.pdf')


            except Exception as e:

                print(e)
                pass
        # count += 1
        # url=url
        # print('next episode..........')

    except Exception as e:
        print("++++++++++++++++++")
        count += 1
        pass
    time.sleep(80)




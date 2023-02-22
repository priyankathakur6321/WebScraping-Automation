import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import sys
import os.path
import textract
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("urls_data.csv")
url_list = list(set(url_path['0']))
len_1 = len(url_list)
base_dir = './theapprofessor.org'
count=1
for dt in url_list:
    if dt.startswith('https://youtu.be'):
        pass
    elif dt.endswith('script.html'):
        print('pass',dt)
    else:
        print("Opening Post url number:",str(count)+'/'+str(len_1))
        title1 = ''
        title = ''
        transcript = ''
        audio_path = ''
        audio = ''
        post_date = ''
        file_name = ''
        try:
            print(dt)
            driver.get(dt)
            time.sleep(15)
            title1 = driver.find_element_by_xpath('//div[@class="wpb_wrapper"]')
            title = title1.text
            title = title.replace("\n", "")
            print(title)
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                read_more=driver.find_element_by_xpath('//div[@title="Read More"]')
                read_more.click()
                time.sleep(2)
                transcript = driver.find_element_by_xpath('//div[@class="class="inner-post-entry entry-content"]/div[3]/div[1]/div/div/div[12]')
                transcript1 = transcript.text
                print(transcript1)
            except:
                print('00000000')
                transcript = driver.find_element_by_xpath('//div[@class="vc_row wpb_row vc_inner vc_row-fluid"]/div[1]')
                transcript = transcript.find_elements_by_tag_name('a')
                for x in transcript:
                    transcript_link = x.get_attribute('href')
                print(transcript_link)
                pass


            # date_ = driver.find_element_by_xpath('//time[@class="entry-date published updated"]')
            # date_ = date_.text
            # from dateutil.parser import parse
            #
            # date_ = parse(date_, fuzzy=True)
            # print(date_, 'parse')
            # post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            # print(post_date, "post_date")
            file_name = title.replace(" ", "_")
            time.sleep(10)
            try:
                audio_path = driver.find_element_by_xpath('//div[@class="wpb_wrapper"]/p/iframe')
                audio_path = audio_path.get_attribute('src')
                print(audio_path, 'aaaaaa')
                driver.get(audio_path)
                time.sleep(5)
                try:
                    audio = driver.find_element_by_xpath('//*[@id="libsyn-player-element"]')
                    link = audio.get_attribute('src')
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
                except:
                    driver.find_element_by_xpath('//*[@id="download-player"]').click()
                    for i in range(120, 0, -1):
                        sys.stdout.write("\r")
                        sys.stdout.write("{:2d} seconds remaining.".format(i))
                        sys.stdout.flush()
                        time.sleep(1)
                    filepath = '/home/webtunixi5/Downloads'
                    filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
                    print(filename)
                    time.sleep(10)
                    shutil.move(os.path.join('.', filename),   'output.mp3')
                    print("done....")

                os.rename("output.mp3", file_name + ".mp3")
                print()
                try:
                    driver.get(transcript_link)
                    time.sleep(5)
                    transcript=driver.find_element_by_xpath('//div[@class="wpb_column vc_column_container vc_col-sm-8"]/div/div')
                    transcript=transcript.text#class="wpb_text_column wpb_content_element wpb_animate_when_almost_visible wpb_flipInX flipInX vc_custom_1584200466829 wpb_start_animation animated"
                except:
                    transcript=transcript1
                with open(file_name + '_orig.txt', 'w') as f:
                    for line in transcript:
                        f.write(line)
                with open(file_name + '.txt', 'w') as f:
                    for line in title:
                        f.write(line)
                with open(file_name + '_info.txt', 'w') as f:
                    f.write(dt + '\n')
                    # f.write(post_date)
                print("Scraped transcript data")
                path = os.path.join(base_dir, file_name)
                os.mkdir(path)
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

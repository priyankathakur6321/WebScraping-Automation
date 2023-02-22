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
base_dir = 'weteachlang.com'
count=1
# driver.maximize_window()
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".docx", 'wb')
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
        try:
            title1 = driver.find_element_by_xpath('//div[@class="vc_custom_heading base_font_color text_align_left"]/h2')
        except:
            title1 = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/h1')
        title = title1.text
        print(title)

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n", "_")
        if os.path.exists(base_dir + '/' + file_name):
            pass
        else:
            # date_ = driver.find_element_by_xpath('//div[@class="col-xs-12 main-header"]/p[2]')
            # date_ = date_.text
            # from dateutil.parser import parse
            #
            # date_ = parse(date_, fuzzy=True)
            # print(date_, 'parse')
            # post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            # print(post_date, "post_date")
            # time.sleep(3)

            # driver.find_element_by_link_text('Download Transcript').click()
            time.sleep(3)
            try:

                transcript_link=driver.find_element_by_link_text('Download Transcript')

            except:
                try:
                    transcript_link=driver.find_element_by_xpath('//div[@class="wpb_text_column"]/p[3]/a')
                except:
                    transcript_link=driver.find_element_by_xpath('//div[@class="wpb_text_column"]/p[3]/strong/a')

            transcript_link = transcript_link.get_attribute('href')

            print(transcript_link)
            time.sleep(4)

            try:
                try:
                    audio_lnk = driver.find_element_by_link_text('Listen to Episode')
                except:
                    try:
                        audio_lnk = driver.find_element_by_xpath('//div[@class="wpb_text_column"]/p[1]/a')
                    except:
                        audio_lnk = driver.find_element_by_xpath('//div[@class="wpb_text_column"]/blockquote/p/a')
                audio_lnk = audio_lnk.get_attribute('href')
                print(audio_lnk,"audio")
                driver.get(audio_lnk)
                time.sleep(5)
                aud=driver.find_element_by_xpath('//div[@class="mejs-mediaelement"]/mediaelementwrapper/audio')
                aud=aud.get_attribute('src')
                print(aud,'dsahgfj')
                time.sleep(4)
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
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

                response = requests.get(aud, params=params,headers=headers)

                response.raise_for_status()
                print('download..')

                # assert response.headers["Content-Type"] == "audio/mpeg"
                with open("output.mp3", "wb") as file:
                    file.write(response.content)
                print("Done.")

                os.rename("output.mp3", file_name + ".mp3")
                download_file(transcript_link, "transcript")
                time.sleep(2)
                transcript = textract.process('transcript.docx')
                print(transcript)
                time.sleep(4)

                path = os.path.join(base_dir, file_name)
                os.mkdir(path)

                print(transcript)
                with open(file_name + '_orig.txt', 'wb') as f:
                    f.write(transcript)
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
                if os.path.exists('./transcript.docx'):
                    os.remove('./transcript.docx')


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




import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("urls_hazeldenbettyford_data.csv")
url_list = list(url_path['0'])
base_dir = './hazeldenbettyford.org'

for i in url_list:
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    try:
        print(i)
        driver.get(i)
        time.sleep(10)
        title1 = driver.find_element_by_xpath('//*[@id="mainform"]/div[4]/div[2]/div[2]/section/div[2]/h1')
        title = title1.text
        print(title)
        transcript = driver.find_element_by_xpath('//*[@id="mainform"]/div[4]/div[2]/div[3]/section/article')
        transcript = transcript.text
        date_ = driver.find_element_by_xpath('//*[@id="body_0_publishedDateSpan"]')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")
        file_name = title.replace(" ", "_")
        time.sleep(10)
        try:
            try:
                audio_path = driver.find_element_by_xpath('//div[@class="cn_copy-with-sidebar with-bar"]/section/article/p[2]/iframe')
                audio_path = audio_path.get_attribute('src')
                print(audio_path, 'aaaaaa')
            except:
                audio_path = driver.find_element_by_xpath(
                    '//div[@class="cn_copy-with-sidebar with-bar"]/section/article/iframe')
                audio_path = audio_path.get_attribute('src')
                print(audio_path, 'bbbbb')
                pass
            driver.get(audio_path)
            time.sleep(10)
            # driver.find_element_by_xpath('//*[@id="download"]').click()
            driver.find_element_by_xpath('//*[@id="download-player"]').click()
            time.sleep(120)
            filepath = '/home/webtunixi5/Downloads'
            filename = max([filepath + "/"+ f for f in os.listdir(filepath)], key=os.path.getctime)
            print(filename)
            time.sleep(30)
            shutil.move(os.path.join('.', filename), file_name + ".mp3")
            time.sleep(10)
            path = os.path.join(base_dir, file_name)
            print(path)
            os.mkdir(path)
            with open(file_name + '_orig.txt', 'w') as f:
                for line in transcript:
                    f.write(line)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(i + '\n')
                f.write(post_date)
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
    except Exception as e:
        print("++++++++++++++++++")
        pass
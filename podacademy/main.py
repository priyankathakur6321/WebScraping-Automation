import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
from datetime import datetime
import os.path
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("./urls_podacademy_data.csv")
url_list = list(url_path['0'])
base_dir = './podacademy.org'


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
        title1 = driver.find_element_by_xpath('//h1[@class="entry-title"]')
        title = title1.text
        print(title)
        transcript = driver.find_element_by_xpath('//div[@class="entry-content"]')
        transcript = transcript.text
        date_ = driver.find_element_by_xpath('//div[@class="entry-meta"]/p[1]')
        date_ = date_.text
        from dateutil.parser import parse

        date_ = parse(date_, fuzzy=True)
        print(date_, 'parse')
        post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        print(post_date, "post_date")



        try:
            file_name = title.replace(" ", "_")
            audio = driver.find_element_by_xpath('//p[@class="powerpress_links powerpress_links_mp3"]/a[2]')
            print(audio, 'data')
            link = audio.get_attribute('href')
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

            assert response.headers["Content-Type"] == "audio/mpeg"
            with open("output.mp3", "wb") as file:
                file.write(response.content)
            print("Done.")

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
                f.write(i + '\n')
                f.write(post_date)
            print("Scraped transcript data")

            shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
            print('audio moved successful')
            shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
            shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
            shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
            print("All data scraped...")
        except Exception as e:
            print(e)
            if os.path.exists("./output.mp3"):
                os.remove("./output.mp3")
            pass
    except:
        print("++++++++++++++++++")
        pass

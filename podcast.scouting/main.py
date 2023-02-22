import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("./urls_prodcastScouting_data.csv")
url_list = list(set(url_path['0']))
base_dir = './prodcast.scouting.org'


for i in url_list:
    try:
        print(i)
        driver.get(i)
        time.sleep(10)
        title1 = driver.find_element_by_xpath('//h1[@class="elementor-heading-title elementor-size-default"]')
        title1 = title1.text
        print(title1)
        transcript_pdf = driver.find_element_by_xpath('/html/body/main/div/div/section[2]/div/div/div/div/div/div[1]/div/p[2]/a')
        transcript_pdf= transcript_pdf.get_attribute('href')



        try:
            try:
                title2 = driver.find_element_by_xpath('/html/body/main/div/div/section[2]/div/div/div/div/div/div[1]/div/p[1]')
                title = title1 + os.linesep + title2.text
            except:
                title = title1
            file_name = title1.replace(" ", "_")
            print(title)
            audio = driver.find_element_by_xpath('/html/body/main/div/div/section[2]/div/div/div/div/div/div[1]/div/p[4]/a[2]')
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

            response1 = requests.get(transcript_pdf)
            with open(file_name + '_orig.txt', 'w') as f:
                f.write(response1.content)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)


            print("Scraped transcript data")

            shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
            print('audio moved successful')
            shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
            shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
        except Exception as e:
            print(e)
            if os.path.exists("./output.mp3"):
                os.remove("./output.mp3")
            pass
    except:
        print("++++++++++++++++++")
        pass

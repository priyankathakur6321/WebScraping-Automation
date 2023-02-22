import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
driver = webdriver.Chrome('../chromedriver')
action = ActionChains(driver)
url_path=pd.read_csv("./urls_midlandsda.csv")
url_list=list(set(url_path['0']))
base_dir='./midlandsda.org'
for i in url_list:
    try:
        print(i)
        driver.get(i)
        time.sleep(10)
        try:
            title=driver.find_element_by_xpath('//h1[@class="entry-title"]')
            title=title.text
            file_name=title.replace(" ", "_")
            print(title)
            audio=driver.find_element_by_xpath('//p[@class="powerpress_links powerpress_links_mp3"]')
            audio=audio.find_elements_by_tag_name('a')
            for x in audio:
                link = x.get_attribute('href')

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

            try:
                trans=driver.find_element_by_xpath('//div[@class="entry-content"]/p[3]/a[2]')
            except:
                trans=driver.find_element_by_xpath('//div[@class="entry-content"]/p[3]/a[1]')
            print(trans.text,"sssss")
            trans=trans.get_attribute('href')
            driver.get(trans)
            time.sleep(4)
            transcript=driver.find_element_by_xpath('//div[@class="WordSection1"]')
            transcript=transcript.text
            with open(file_name+ 'orig.txt', 'w') as f:
                for line in transcript:
                    f.write(line)
            with open(file_name+ '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            print("Scraped transcript data")
            os.rename("output.mp3", file_name + ".mp3")
            path = os.path.join(base_dir, file_name)
            os.mkdir(path)
            shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
            print('audio moved successful')
            shutil.move(file_name+ 'orig.txt', path + '/' + file_name + 'orig.txt')
            shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
        except Exception as e:
            print(e)
            if os.path.exists("./output.mp3"):
                os.remove("./output.mp3")
            pass
    except:
        print("++++++++++++++++++")
        pass


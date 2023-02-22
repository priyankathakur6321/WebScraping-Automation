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
url_path = pd.read_csv("./urls_pnas_data.csv")
url_list = list(set(url_path['0']))
base_dir = './pnas.org'
for i in url_list:
    try:
        print(i)
        driver.get(i)
        time.sleep(10)
        title1 = driver.find_element_by_xpath('//*[@id="frontmatter"]/header/div/h1')
        title1 = title1.text
        transcript = driver.find_element_by_xpath('//*[@id="bodymatter"]/div')
        transcript = transcript.text
        if transcript is None:
            pass
        else:
            try:
                try:
                    title2 = driver.find_element_by_xpath('//*[@id="frontmatter"]/header/div/p')
                    title = title1 + os.linesep + title2.text
                except:
                    title = title1
                file_name = title1.replace(" ", "_")
                print(title)
                try:
                    audio_path = driver.find_element_by_xpath('//*[@id="pb-page-content"]/div/div/main/div[1]/div/article/section[2]/div/div/iframe')
                    audio_path = audio_path.get_attribute('src')
                    print(audio_path,'aaaaaa')
                except:
                    print("no")
                    pass
                driver.get(audio_path)
                time.sleep(10)
                audio = driver.find_element_by_xpath('/html/head/meta[11]')
                print(audio, 'data')
                link = audio.get_attribute('content')
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

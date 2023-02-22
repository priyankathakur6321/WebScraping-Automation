import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import docx2txt
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("urls_data.csv")
url_list = list(url_path['0'])
base_dir = './ctcfp.org'

for i in url_list:
    title1 = ''
    title = ''
    transcript = ''
    audio_path = ''
    audio = ''
    post_date = ''
    file_name = ''
    try:
        print(i)
        driver.get(i)
        time.sleep(5)
        CHECK=driver.find_element_by_xpath('//li[@class="jupiterx-post-meta-categories list-inline-item"]/a')
        CHECK=CHECK.text
        if CHECK=="Podcasts":
            title1 = driver.find_element_by_xpath('//div[@class="container-fluid"]/h1')
            title = title1.text
            print(title)
            # transcript = driver.find_element_by_xpath('//div[@class="jet-button__container"]/a')
            # transcript = transcript.get_attribute('href')
            date_ = driver.find_element_by_xpath('//li[@class="jupiterx-post-meta-date list-inline-item"]/time')
            date_ = date_.text
            from dateutil.parser import parse

            date_ = parse(date_, fuzzy=True)
            print(date_, 'parse')
            post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            print(post_date, "post_date")
            file_name = title.replace(" ", "_")
            if os.path.exists('./ctcfp.org/' + file_name):
                pass
            else:
                time.sleep(10)
                try:
                    try:
                        try:
                            audio_path = driver.find_element_by_xpath('//div[@class="jet-button__container"]/a')
                        except:
                            audio_path = driver.find_element_by_xpath('//div[@class ="jupiterx-content"]/article/div/div[1]/ul/li[1]/a')
                    except:
                        audio_path = driver.find_element_by_xpath('//div[@class="jupiterx-post-content clearfix"]/div/div[1]/a')
                    link = audio_path.get_attribute('href')
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
                    try:
                        try:
                            driver.find_element_by_xpath('//div[@class="elementor-container elementor-column-gap-default"]/div[2]/div/div/div/div/div/a/div[4]/span').click()
                        except:
                            driver.find_element_by_xpath('//div[@class ="jupiterx-content"]/article/div/div[1]/ul/li[2]/a').click()
                    except:
                        try:
                            driver.find_element_by_xpath('//div[@class="jupiterx-post-content clearfix"]/ul/li[1]/a').click()
                        except:
                            driver.find_element_by_xpath('//div[@class="jupiterx-post-content clearfix"]/div/div[2]/a').click()
                    time.sleep(20)
                    filepath = '/home/webtunixi5/Downloads'
                    filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
                    print(filename)
                    time.sleep(10)
                    shutil.move(os.path.join('.', filename), file_name + '_orig.docx')
                    text = docx2txt.process(file_name + '_orig.docx')
                    time.sleep(5)
                    with open(file_name + '_orig.txt', 'w') as f:
                        for line in text:
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
                    if os.path.exists('./'+file_name + '_orig.docx'):
                        os.remove('./'+file_name + '_orig.docx')
                except Exception as e:
                    print(e)
                    pass
        else:
            print("Not a podcast.")
            pass
    except Exception as e:
        print("++++++++++++++++++")
        pass
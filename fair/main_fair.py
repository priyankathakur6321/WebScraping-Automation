import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import urllib.request
import re
import os.path

driver = webdriver.Chrome('../chromedriver')
action = ActionChains(driver)
url_path = pd.read_csv("./urls_fair_data.csv")
url_list = list(set(url_path['0']))
for i in url_list:
    try:
        print(i)
        driver.get(i)
        time.sleep(10)
        try:

            driver.find_element_by_xpath('//span[@class="bars_mp3j"]').click()
        #     try:
        #         text = "audio_file"
        #         params = {
        #             "ie": "UTF-8",
        #             "client": "tw-ob",
        #             "q": text,
        #             "tl": "en",
        #             "total": "1",
        #             "idx": "0",
        #             "textlen": str(len(text))
        #         }
        #         response = requests.get(link, params=params)
        #         response.raise_for_status()
        #
        #         assert response.headers["Content-Type"] == "audio/mpeg"
        #         with open("output.mp3", "wb") as file:
        #             file.write(response.content)
        #         print("Done.")
        #     except:
        #         print("Getting an error.")
        #         pass
        except:
            pass

        # print(url, "Url")
        # a = url.find_elements_by_tag_name('a')
        # for x in a:
        #     link = x.get_attribute('href')
        #     list_1.append(link)
    except:
        print('=======================')

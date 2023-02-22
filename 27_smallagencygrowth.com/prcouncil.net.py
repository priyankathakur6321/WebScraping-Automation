

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Chrome(ChromeDriverManager().install())

# driver = webdriver.Chrome('./chromedriver')
action = ActionChains(driver)
url='https://prcouncil.net/agencies-future-podcast/'
indx = 1
list_main=[]
podcast_list=[]
try:
    print(url)
    driver.get(url)
    time.sleep(4)
    podcast=driver.find_element_by_xpath('//*[@id="post-20981"]/div/div/div[2]/div[2]/ul')
    time.sleep(5)
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        podcast_list.append(link)

except Exception as e:
    print(e)
    pass


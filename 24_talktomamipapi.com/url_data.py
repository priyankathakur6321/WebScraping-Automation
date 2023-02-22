
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
list_main=[]
url='https://www.talktomamipapi.com/episodes/'
indx = 2
final_list=[]
try:
    print(url)
    driver.get(url)
    time.sleep(4)
    # driver.find_element_by_xpath('//*[@id="yui_3_17_2_1_1652808873495_487"]').click()
    # time.sleep(2)
    full_url = driver.find_element_by_xpath('//div[@class="blog-side-by-side-wrapper"]')
    a = full_url.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        list_main.append(link)
    time.sleep(2)
    while True:
        try:
            driver.find_element_by_xpath('//div[@class="older"]/a').click()
            time.sleep(5)
        except:
            driver.find_element_by_xpath('//nav[@class="blog-list-pagination"]/div[2]/a').click()
            time.sleep(5)
        full_url = driver.find_element_by_xpath('//div[@class="blog-side-by-side-wrapper"]')
        a = full_url.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            print(link)
            list_main.append(link)
        time.sleep(2)
except Exception as e:
    print(e)
    pass

print(len(set(list_main)),"final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_data.csv')


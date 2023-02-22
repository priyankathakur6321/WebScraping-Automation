import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# driver = webdriver.Chrome('./chromedriver')
action = ActionChains(driver)
base_list=[]
indx=2
try:
    driver.get('https://podcast.clearhq.org/')
    time.sleep(4)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        load_more=driver.find_element_by_xpath('//*[@id="load_more"]')
        time.sleep(4)
        load_more.click()
        time.sleep(5)

        try:
            full_url = driver.find_element_by_xpath('//*[@id="container"]/div[3]')
            a = full_url.find_elements_by_tag_name('a')
            for x in a:
                link = x.get_attribute('href')
                print(link)
                base_list.append(link)
        except :
            print('opps error')
            pass
except Exception as e:
    print(e)
    pass
base_list=set(base_list)
print(len(base_list),"final....#####")
df = pd.DataFrame(base_list)
df.to_csv('urls_prodcastClearhq_data.csv')










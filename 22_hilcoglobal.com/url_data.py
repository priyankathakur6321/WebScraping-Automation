
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
url='https://www.hilcoglobal.com/smarter-perspectives/'
indx = 2
try:

    while indx!=15:
        print(url)
        driver.get(url)
        time.sleep(4)
        full_url = driver.find_element_by_xpath('//*[@id="Contentplaceholder1_C015_Col00"]/div[2]')
        a = full_url.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            list_main.append(link)
            print(link)
        url='https://www.hilcoglobal.com/smarter-perspectives/'
        url=url+str(indx)
        indx+=1
except Exception as e:
    print(e)
    pass
list_main=set(list_main)
print(len(list_main),"final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_data.csv')



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
url='https://www.dvinci.com/blog?field_blogpost_type_target_id=All&page='
indx = 0
final_list=[]
try:
    while indx!=15:
        print(url)
        driver.get(url+str(indx))
        time.sleep(4)

        full_url = driver.find_element_by_xpath('//div[@class="thinkingindex-results"]')
        a = full_url.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            print(link)
            list_main.append(link)
        time.sleep(2)
        indx+=1
        continue
except Exception as e:
    print(e)
    pass

print(len(set(list_main)),"final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_data.csv')


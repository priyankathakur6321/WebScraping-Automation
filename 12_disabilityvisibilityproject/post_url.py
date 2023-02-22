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
url='https://disabilityvisibilityproject.com/podcast-2/'
indx=2

try:
    driver.get(url)
    time.sleep(4)


    full_url = driver.find_element_by_xpath('//div[@class="the-content"]')
    a = full_url.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        if link is None or link.endswith('.png'):
            pass
        else:
            list_main.append(link)
            print(link)

except Exception as e:
    print(e)
    pass

list_main=set(list_main)
print(len(list_main),"final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_data.csv')



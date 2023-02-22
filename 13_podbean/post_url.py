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
list_1=[]
url='https://www.podbean.com/all'
indx=2

try:
    driver.get(url)
    time.sleep(4)
    try:
            full_url = driver.find_element_by_xpath('//div[@class="span9 category-all-left"]')
            a = full_url.find_elements_by_tag_name('a')
            for x in a:
                link = x.get_attribute('href')
                driver.get(link)
                time.sleep(4)
                prodcast_url =driver.find_element_by_xpath('//div[@class="top-podcasts"]')
                a = prodcast_url.find_elements_by_tag_name('a')
                for x in a:
                    link = x.get_attribute('href')
                    if link is None or link.endswith('.png'):
                        pass
                    else:
                        list_1.append(link)
                        print(link)

    except:
        pass

except Exception as e:
    print(e)
    pass

list_main1=set(list_1)
print(len(list_main1),"final....#####")
df = pd.DataFrame(list_main1)
df.to_csv('urls_data.csv')



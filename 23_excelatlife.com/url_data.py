
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
url='https://www.excelatlife.com/default.htm'
indx = 2
final_list=[]
try:
    print(url)
    driver.get(url)
    time.sleep(4)
    xpath='//*[@id="content"]/div/div['
    while indx!=20:
        full_url = driver.find_element_by_xpath(xpath+str(indx)+']/div')
        a = full_url.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            print(link)
            list_main.append(link)
            # try:
            #     driver.get(link)
            #     time.sleep(5)
            #     next_url=driver.find_element_by_xpath('//*[@id="page_content"]/div')
            #     a2 = next_url.find_elements_by_tag_name('a')
            #     for x1 in a2:
            #         link1 = x1.get_attribute('href')
            #         list_main.append(link1)
            #         print(link1)
            #     pass
            # except:
            #     list_main.append(link)
            #     pass
        # driver.get(link)
        time.sleep(2)
        indx+=1
        continue
except Exception as e:
    print(e)
    pass
list_main=set(list_main)
for urlq in list_main:
    try:
        driver.get(urlq)
        time.sleep(3)
        url_tag=driver.find_element_by_xpath('//*[@id="page_content"]/div')
        a2 = url_tag.find_elements_by_tag_name('a')
        for x1 in a2:
            link1 = x1.get_attribute('href')
            final_list.append(link1)
            print(link1)
        pass
    except:
        final_list.append(urlq)
        pass
print(len(set(final_list)),"final....#####")
df = pd.DataFrame(final_list)
df.to_csv('urls_data.csv')


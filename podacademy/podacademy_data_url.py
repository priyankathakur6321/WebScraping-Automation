import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# driver = webdriver.Chrome('./chromedriver')
action = ActionChains(driver)
list_1=[]
base_list=[]
indx=2
try:
    driver.get('https://podacademy.org/')
    time.sleep(4)
    full_url = driver.find_element_by_xpath('//*[@id="menu-main-navigation"]')
    a = full_url.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        base_list.append(link)
    print(len(base_list))
except Exception as e:
    print(e)
    pass
for i in base_list:
    try:
        driver.get(i)
        try:

            data_link=driver.find_element_by_xpath('//*[@id="primary"]')
            r = data_link.find_elements_by_tag_name('a')
            for x1 in r:
                link1 = x1.get_attribute('href')
                print(link1)
                list_1.append(link1)
            while True:
                driver.find_element_by_xpath('//*[@id="nav-below"]/div[1]/a"]').click()
                data_link = driver.find_element_by_xpath('//*[@id="primary"]')
                r = data_link.find_elements_by_tag_name('a')
                for x1 in r:
                    link1 = x1.get_attribute('href')
                    print(link1)
                    list_1.append(link1)
        except:
            pass

    except Exception as e:
        print("////////",e)
        pass
list_main=set(list_1)
print(len(list_main),"final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_podacademy_data.csv')










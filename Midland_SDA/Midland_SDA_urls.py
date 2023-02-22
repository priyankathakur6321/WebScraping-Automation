import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Chrome('../chromedriver')
action = ActionChains(driver)
# base_dir = './midlandsda.org'
list_1=[]



try:
    driver.get('https://www.midlandsda.org/blog/')
    time.sleep(4)

    try:
        secondary_url=driver.find_element_by_xpath('//*[@id="categories-4"]/ul')
        secondary_a=secondary_url.find_elements_by_tag_name('a')
        print("opening secondary")

        list_secondary=[]
        for x in secondary_a:
            link = x.get_attribute('href')
            print(link)
            list_secondary.append(link)
        for i in list_secondary:
            print(i,"secondary......")
            try:
                driver.get(i)
                time.sleep(4)
                prd_url=driver.find_element_by_xpath('//*[@id="primary"]')
                prd_url = prd_url.find_elements_by_tag_name('a')
                for x in prd_url:
                    link = x.get_attribute('href')

                    print(link,"secondary_links")
                    list_1.append(link)
            except:
                pass

    except Exception as e:
        print("got error:",e)
        pass
    while True:

        Primary_url = driver.find_element_by_xpath('//*[@id="content"]')
        primary_a = Primary_url.find_elements_by_tag_name('a')
        for x in primary_a:
            link = x.get_attribute('href')

            print(link, "primary_link")
            list_1.append(link)

        driver.find_element_by_xpath('//*[@id="nav-below"]/div[1]/a').click()
    else:
        pass


except Exception as e:
    print('=======================')
    print(e)
    pass
list_1=set(list_1)
df = pd.DataFrame(list_1)
df.to_csv('urls_midlandsda.csv')



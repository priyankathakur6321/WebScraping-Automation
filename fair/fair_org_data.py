import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Chrome('../chromedriver')
action = ActionChains(driver)
list_1=[]

page_itr=2
next_page='https://fair.org/home/page/'
try:

    driver.get('https://fair.org/home/')
    time.sleep(4)
    while page_itr!=226:
        url = driver.find_element_by_xpath('//main[@class="content"]')
        a = url.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            if link == None:
                # print("None link found")
                pass
            else:
                if "https://fair.org/home/page/" not in link:
                    print(link)
                    list_1.append(link)
                else:
                    print("contain page url",link)
                    pass
        link_next = next_page+str(page_itr)
        driver.get(link_next)
        page_itr+=1
    else:
        pass



except Exception as e:
    print('=======================')
    print(e)
    pass
list_1=set(list_1)
df = pd.DataFrame(list_1)
df.to_csv('urls_fair_data.csv')



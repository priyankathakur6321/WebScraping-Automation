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
indx=2
try:
    driver.get('https://humanitiesny.org/news/')
    time.sleep(4)
    full_url = driver.find_element_by_xpath('/html/body/div/div[2]/div/aside')
    a = full_url.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        if link == None:
            pass
        else:
            print(link)
            list_1.append(link)
    while indx != 9:
        try:
            url = driver.find_element_by_xpath('/html/body/div/div[2]/div/main')
            a = url.find_elements_by_tag_name('a')
            for x in a:
                link = x.get_attribute('href')
                if link == None:
                    pass
                else:
                    print(link)
                    list_1.append(link)
        except Exception as e:
            print(e)
            pass


        current_page='https://humanitiesny.org/news/page/'
        driver.get(current_page+str(indx)+'/')
        indx+=1
    else:
        pass
except Exception as e:
    print(e)
    pass
list_1=set(list_1)
df = pd.DataFrame(list_1)
df.to_csv('urls_humanitiesny_data.csv')







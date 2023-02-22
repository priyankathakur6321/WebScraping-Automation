import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Chrome(ChromeDriverManager().install())

# driver = webdriver.Chrome('./chromedriver')
action = ActionChains(driver)
list_main=[]
url='https://www.ctcfp.org/posts/'
indx=2
try:
    driver.get(url)
    time.sleep(10)
    full_url = driver.find_element_by_xpath('//div[@class="elementor-posts-container elementor-posts elementor-posts--skin-cards elementor-grid elementor-has-item-ratio"]')
    a = full_url.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        if link is None or link.endswith('.png'):
            pass
        else:
            list_main.append(link)
            print(link)
    while True:

        driver.get(url+'page/'+str(indx))
        time.sleep(10)
        full_url = driver.find_element_by_xpath(
            '//div[@class="elementor-posts-container elementor-posts elementor-posts--skin-cards elementor-grid elementor-has-item-ratio"]')
        a = full_url.find_elements_by_tag_name('a')
        for x in a:
            link = x.get_attribute('href')
            if link is None or link.endswith('.png'):
                pass
            else:
                list_main.append(link)
                print(link)
        indx+=1

except Exception as e:
    print(e)
    pass

list_main=set(list_main)
for i in list_main:
    driver.get(i)

print(len(list_main),"final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_data.csv')



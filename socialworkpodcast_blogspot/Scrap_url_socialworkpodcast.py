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
indx=2
try:
    driver.get('https://socialworkpodcast.blogspot.com/')
    time.sleep(4)
    full_url = driver.find_element_by_xpath('//div[@class="blog-posts hfeed"]')
    a = full_url.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        if link == None:
            pass
        else:
            print(link)
            if link.endswith(".html") or link.endswith(".html#more"):
                list_main.append(link)
            else:
                print(link,"not a blog post link")
    while True:
            driver.find_element_by_xpath('//*[@id="blog-pager-older-link"]').click()
            full_url = driver.find_element_by_xpath('//div[@class="blog-posts hfeed"]')
            a = full_url.find_elements_by_tag_name('a')
            for x in a:
                link = x.get_attribute('href')
                if link == None:
                    pass
                else:
                    print(link)

                    if link.endswith(".html"):
                        list_main.append(link)
                    else:
                        print(link, "not a blog post link")
except Exception as e:
    print(e)
    pass

list_main=set(list_main)
print(len(list_main),"final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_socialworkpodcast_data.csv')



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
url='https://www.smallagencygrowth.com/directory/podcasts/'
indx = 1
list_main=[]
podcast_list=[]
try:
    print(url)
    driver.get(url)
    time.sleep(4)
    podcast=driver.find_element_by_xpath('//div[@class="elementor-widget-container"]/ul')
    time.sleep(5)
    a = podcast.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        podcast_list.append(link)
    for podcast_url in podcast_list:
        driver.get(podcast_url)
        time.sleep(5)
        data = driver.find_element_by_xpath('//section[@class="Main-content"]/section')
        a2 = data.find_elements_by_tag_name('a')
        for x1 in a2:
            link1 = x1.get_attribute('href')
            print(link1)
            list_main.append(link1)
        load_more = driver.find_element_by_xpath('//section[@class="Main-content"]/nav/a')
        link_more = load_more.get_attribute('href')
        time.sleep(4)
        driver.get(link_more)
        time.sleep(5)
        data = driver.find_element_by_xpath('//section[@class="Main-content"]/section')
        a2 = data.find_elements_by_tag_name('a')
        for x1 in a2:
            link1 = x1.get_attribute('href')
            print(link1)
            list_main.append(link1)
        try:
            while True:
                load_more=driver.find_element_by_xpath('//section[@class="Main-content"]/nav/a[2]')
                link_more=load_more.get_attribute('href')
                time.sleep(4)
                driver.get(link_more)
                time.sleep(5)
                data=driver.find_element_by_xpath('//section[@class="Main-content"]/section')
                a2 = data.find_elements_by_tag_name('a')
                for x1 in a2:
                    link1 = x1.get_attribute('href')
                    print(link1)
                    list_main.append(link1)
                continue
        except:
            pass

except Exception as e:
    print(e)
    pass

print(list_main)
print(len(set(list_main)),"final....#####")
df = pd.DataFrame(list_main)
df.to_csv('2bbs_com_urls_data.csv')
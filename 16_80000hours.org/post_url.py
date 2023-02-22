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
list_main = []
list_1 = []
url = 'https://80000hours.org/podcast/'
indx = 2

try:
    driver.get(url)
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="navigation-topics"]/div/div[1]/h5/a').click()
    driver.find_element_by_xpath('//*[@id="navigation-podcast-interviewee"]/div/div[1]/h5/a').click()
    driver.find_element_by_xpath('//*[@id="navigation-podcast-date"]/div/div[1]/h5/a').click()
    try:
        topic_url = driver.find_element_by_xpath('//*[@id="navigation-topics--collapse"]')
        a = topic_url.find_elements_by_tag_name('a')
        count = 1
        for x in a:
            link = x.get_attribute('href')
            print(count, ">>>", link)
            list_1.append(link)
    except Exception as e:
        print("Error in topic url", e)
        pass
    try:
        interview_url = driver.find_element_by_xpath('//*[@id="navigation-podcast-interviewee--collapse"]')
        a = interview_url.find_elements_by_tag_name('a')
        count = 1
        for x in a:
            link = x.get_attribute('href')
            print(count, ">>>", link)
            list_main.append(link)
            count += 1
    except Exception as e:
        print("Error in Interview url", e)
        pass
    try:
        podcastdate_url = driver.find_element_by_xpath('//*[@id="navigation-podcast-date--collapse"]')
        a = podcastdate_url.find_elements_by_tag_name('a')
        count = 1
        for x in a:
            link = x.get_attribute('href')
            print(count, ">>>", link)
            list_main.append(link)
            count += 1
    except Exception as e:
        print("Error in podcastdate url", e)
        pass
    for i in list_1:
        try:
            print("asdfgh",i)
            driver.get(i)
            individual_topic_url = driver.find_element_by_xpath('//*[@id="navigation-list-everything--collapse"]')
            a = individual_topic_url.find_elements_by_tag_name('a')
            count = 1
            for x in a:
                link = x.get_attribute('href')
                print(count, ">>>", link)
                list_main.append(link)
                count += 1
        except Exception as e:
            print("Error in individual_topic_url url", e)
            pass
except Exception as e:
    print(e)
    pass

list_main = set(list_main)
print(len(list_main), "final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_data.csv')

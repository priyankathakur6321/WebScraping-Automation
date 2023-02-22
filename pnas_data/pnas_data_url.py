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
indx=0
try:
    driver.get('https://www.pnas.org/about/science-sessions-podcast')
    time.sleep(4)
    while indx != 40:
        try:
            url = driver.find_element_by_xpath('//div[@class="card-columns"]')
            a = url.find_elements_by_tag_name('a')
            for x in a:
                link = x.get_attribute('href')
                if link == None:
                    pass
                else:
                    print(link)
                    list_1.append(link)
            full_epi=driver.find_element_by_xpath('//div[@class="d-flex justify-content-end animation-icon-shift"]')
            full_epi=full_epi.find_element_by_tag_name('a')
            full_epi_link=full_epi.get_attribute('href')
            print(full_epi_link,'full_epi_link')
            driver.get(full_epi_link)
            full_url = driver.find_element_by_xpath('//div[@class=" search-result__body titles-results "]')
            a = full_url.find_elements_by_tag_name('a')
            for x in a:
                link = x.get_attribute('href')
                if link == None:
                    pass
                else:
                    print(link)
                    list_1.append(link)
        except:
            full_url = driver.find_element_by_xpath('//div[@class=" search-result__body titles-results "]')
            a = full_url.find_elements_by_tag_name('a')
            for x in a:
                link = x.get_attribute('href')
                if link == None:
                    pass
                else:
                    print(link)
                    list_1.append(link)

        current_page='https://www.pnas.org/all-posts/science-sessions-podcast?startPage='
        driver.get(current_page+str(indx+1)+'&pageSize=20')
        indx+=1
    else:
        pass
except Exception as e:
    print(e)
    pass
list_1=set(list_1)
df = pd.DataFrame(list_1)
df.to_csv('urls_pnas_data.csv')







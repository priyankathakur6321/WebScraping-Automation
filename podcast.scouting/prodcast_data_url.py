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
    driver.get('https://podcast.scouting.org/')
    time.sleep(4)
    full_url = driver.find_element_by_xpath('/html/body/main/div/div/div/section[2]/div/div/div/div/div/section/div/div')
    a = full_url.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        base_list.append(link)
except Exception as e:
    print(e)
    pass
for i in base_list:
    try:
        driver.get(i)
        try:

            data_link=driver.find_element_by_xpath('//div[@class="elementor-posts-container elementor-posts elementor-posts--skin-cards elementor-grid elementor-has-item-ratio"]')
            r = data_link.find_elements_by_tag_name('a')
            for x1 in r:
                link1 = x1.get_attribute('href')
                print(link1)
                list_1.append(link1)
            while indx != 8:
                current_page=link
                try:
                    driver.get(current_page+"page/"+str(indx)+'/')
                except:
                    pass
                indx+=1
            else:
                pass
        except:
            pass

    except Exception as e:
        print("////////",e)
        pass
df = pd.DataFrame(list_1)
df.to_csv('urls_prodcastScouting_data.csv')










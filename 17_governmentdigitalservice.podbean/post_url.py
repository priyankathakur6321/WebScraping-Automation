import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.maximize_window()

action = ActionChains(driver)
list_main = []
list_1 = []
url = 'https://governmentdigitalservice.podbean.com/'
indx = 2

try:
    driver.get(url)
    time.sleep(4)
    try:
        episode_url = driver.find_element(By.XPATH, '//div[@class="container"]/div[1]')
        a = episode_url.find_elements(By.TAG_NAME, 'a')
        count = 1
        for x in a:
            link = x.get_attribute('href')
            if link.startswith('https://governmentdigitalservice.podbean.com/'):
                print(count, ">>>", link)
                list_main.append(link)
                count += 1
        page=2
        while page!=5:
            # WebDriverWait(driver, 20).until(
            #     EC.element_to_be_clickable((By.XPATH,'//a[@class="p-2 text-decoration-none"]'))).click()
            driver.get(url+'page/'+str(page)+'/')
            time.sleep(3)
            episode_url=driver.find_element(By.XPATH,'//div[@class="container"]/div[1]')
            a = episode_url.find_elements(By.TAG_NAME,'a')
            count=1
            for x in a:
                link = x.get_attribute('href')
                if link.startswith('https://governmentdigitalservice.podbean.com/'):
                    print(count, ">>>", link)
                    list_main.append(link)
                    count += 1
            page+=1
    except Exception as e:
        print("Error in podcastdate url", e)
        pass
except Exception as e:
    print(e)
    pass

list_main = set(list_main)
print(len(list_main), "final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_data.csv')

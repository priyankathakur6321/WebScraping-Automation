import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# driver = webdriver.Chrome('./chromedriver')
action = ActionChains(driver)
list_main = []
# list_1 = []
# base_dir = './npic.orst.edu'
url = 'https://www.wisconsinhistory.org/HolocaustSurvivors/testimonies.asp'
# indx = 2
try:
    print(url)
    driver.get(url)
    time.sleep(4)
    data=driver.find_element_by_xpath('//*[@id="sidebar-left"]/ul')
    a = data.find_elements_by_tag_name('a')
    for x in a:
        link = x.get_attribute('href')
        print(link)
        list_main.append(link)
except Exception as e:
    print(e)
    pass

list_main = set(list_main)
print(len(list_main), "final....#####")
df = pd.DataFrame(list_main)
df.to_csv('testimonies_urls_data.csv')





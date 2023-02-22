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
action = ActionChains(driver)
title_list=[]
link_media=[]
quicktime_list=[]
trascript_link=[]
url='https://www.ovcttac.gov/victimimpact/presenters_toolbox.cfm?print=1'
try:
    print(url)
    driver.get(url)
    time.sleep(4)
    base_xpath='//*[@id="content_sub_toolbox_left"]/ol'
    t=1
    while True:
        xpath = base_xpath + '/li[' + str(t) + ']'
        data = driver.find_element_by_xpath(xpath)

        title=driver.find_element_by_xpath(xpath+'/strong').text
        title_list.append(title)
        print(title)
        a = data.find_elements_by_tag_name('a')
        # print(a)
        # link1=a.get_attribute('href')
        # print(link1)
        count = 1
        for x in a:
            link = x.get_attribute('href')
            if link.endswith('.wmv'):
                link_media.append(link)
            elif link.endswith('.mov'):
                quicktime_list.append(link)
            elif link.endswith('.pdf'):
                trascript_link.append(link)
            else:
                pass
            count += 1
        time.sleep(4)
        t+=1
    else:
        print("no more data")
        pass
except Exception as e:
    print(e)
    pass
title_list.insert(7,'Unit 9. Child Sexual Abuse part2')
title_list.insert(11,'Unit 12. Homicide part2')
title_list.insert(12,'Unit 12. Homicide part3')
print(len(title_list))
print(len(link_media))
print(len(quicktime_list))
print(len(trascript_link))
main_df = pd.DataFrame(
    {'title': title_list,
     'media_url': link_media,
     'quicktime_media_url': quicktime_list,
     'transcript_pdf': trascript_link
    })
main_df.to_csv('urls_data.csv')
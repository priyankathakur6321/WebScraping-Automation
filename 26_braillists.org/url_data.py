
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
url='https://www.braillists.org/media/'
indx = 1
list_main=[]
media_list=[]
title_list=[]
transcript_list=[]
try:
    print(url)
    driver.get(url)
    time.sleep(4)
    while indx != 100:
        try:
            full_url = driver.find_element_by_xpath('//div[@class="entry-content"]/a['+str(indx)+']')
            link = full_url.get_attribute('href')
            print(link, '++++++++++++')
            if link.endswith('.docx'):
                if link.startswith('https://www.braillists.org/wp-content/uploads/tr'):
                    transcript_list.append(link)
                else:
                    pass
            else:
                pass
        except:
            pass
        try:
            audio_url = driver.find_element_by_xpath('//div[@class="entry-content"]/audio[' + str(indx) + ']')
            link_audio = audio_url.get_attribute('src')
            print('++++++++++++', link_audio)
            title = driver.find_element_by_xpath('//div[@class="entry-content"]/h2[' + str(indx) + ']')
            title = title.text
            if link_audio.endswith('.mp3'):
                media_list.append(link_audio)
                print(title)
                title_list.append(title)
            else:
                pass
        except:
            pass

        time.sleep(2)
        indx+=1
        continue

except Exception as e:
    print(e)
    pass
transcript_list=list(set(transcript_list))
print(media_list,'media list')
print(transcript_list,'transcript_list')
print(len(media_list),'media list')
print(len(transcript_list),'transcript_list')


for xc in transcript_list:
    data_list = []
    comp=xc[-9:]
    print(comp)
    comp=comp.replace('.docx','.mp3')
    print(comp,'compare')
    for index,m_url in enumerate(media_list):
        title_n = title_list[index]
        if m_url.split("/")[-1]==comp:
            data_list.append(m_url)
            data_list.append(xc)
            data_list.append(title_n)
        else:
            pass
    list_main.append(data_list)
print(list_main)
print(len(list_main),"final....#####")
df = pd.DataFrame(list_main)
df.to_csv('urls_data.csv')
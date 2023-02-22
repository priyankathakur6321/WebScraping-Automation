import pandas as pd
import textract
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import docx2txt
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://awesomeatyourjob.libsyn.com/'
action = ActionChains(driver)
url_list = []
skip_list=[]
base_dir = './awesomeatyourjob.libsyn.com'
count=1

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

url_path = pd.read_csv("urls_data.csv")
url_list = list(url_path['0'])
len_1 = len(url_list)
print(url_list)
for aa in range(len_1):
    aa=aa+2270



    za=url_list[aa]
    print(za,'llllllllllllllllllllll')
    print("Opening Post url number:", str(aa) + '/' + str(len_1))
    if za==None:
        print('none url')
        pass
    elif za.startswith('https://awesomeatyourjob.libsyn.com/'):
        driver.get(za)
        title1 = ''
        title = ''
        transcript = ''
        audio_path = ''
        audio = ''
        post_date = ''
        file_name = ''
        try:

            time.sleep(4)
            title1 = driver.find_element_by_xpath('//div[@class="libsyn-item-title"]/a[1]')
            title = title1.text
            print(title)

            file_name = title.replace(" ", "_")
            file_name = file_name.replace("\n", "_")
            if os.path.exists(base_dir + '/' + file_name):
                pass
            else:

                date_ = driver.find_element_by_xpath('//div[@class="libsyn-item-release-date"]')
                date_ = date_.text
                from dateutil.parser import parse

                date_ = parse(date_, fuzzy=True)
                print(date_, 'parse')
                post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
                print(post_date, "post_date")
                time.sleep(3)

                transcript_link=driver.find_element_by_xpath('//div[@class="libsyn-item"]/div[3]')
                transcript_link = transcript_link.find_elements_by_tag_name('a')
                for x2 in transcript_link:
                    link = x2.get_attribute('href')
                    print(link)
                    if link.startswith('http://awesomeatyourjob.com'):
                        trans_link=link
                        print(trans_link,'transcript_link')
                    else:
                        pass

                time.sleep(4)

                try:
                    audio_link=driver.find_element_by_xpath('//div[@class="libsyn-item-player"]/iframe')
                    If_link=audio_link.get_attribute('src')
                    print(If_link)
                    driver.get(If_link)
                    time.sleep(4)
                    audio_lnk = driver.find_element_by_xpath('//*[@id="download-player"]')
                    audio_lnk = audio_lnk.click()
                    time.sleep(4)

                    for i in range(20, 0, -1):
                        sys.stdout.write("\r")
                        sys.stdout.write("{:2d} seconds remaining.".format(i))
                        sys.stdout.flush()
                        time.sleep(1)
                    filepath = '/home/webtunixi5/Downloads'
                    filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
                    print(filename)
                    time.sleep(10)
                    shutil.move(os.path.join('.', filename), 'output.mp3')
                    print("done....")

                    os.rename("output.mp3", file_name + ".mp3")
                    # driver.get(transcript_link)
                    time.sleep(4)


                    path = os.path.join(base_dir, file_name)
                    os.mkdir(path)
                    driver.get(trans_link)
                    time.sleep(3)
                    driver.find_element_by_xpath('//div[@class="toggle default"]/h3/a').click()
                    time.sleep(3)
                    transcript=driver.find_element_by_xpath('//div[@class="toggle default open"]/div/div')
                    transcript=transcript.text
                    print(transcript)
                    with open(file_name + '_orig.txt', 'w') as f:
                        for line in transcript:
                            f.write(line)
                    with open(file_name + '.txt', 'w') as f:
                        for line in title:
                            f.write(line)
                    with open(file_name + '_info.txt', 'w') as f:
                        f.write(za + '\n')
                        f.write(post_date)
                    print("Scraped transcript data")

                    shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
                    print('audio moved successful')
                    shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
                    shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
                    shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
                    print("Done.")
                    if os.path.exists('./transcript.pdf'):
                        os.remove('./transcript.pdf')


                except Exception as e:

                    print(e)
                    pass
            count += 1
            print('next episode..........')

        except Exception as e:
            print("++++++++++++++++++")
            count += 1
            pass
    else:
        print('Episode url not valid')
        count+=1
        pass



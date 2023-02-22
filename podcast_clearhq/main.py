import re
import urllib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os.path
import requests
import shutil
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

driver = webdriver.Chrome(ChromeDriverManager().install())

action = ActionChains(driver)
url_path = pd.read_csv("./urls_prodcastClearhq_data.csv")
url_list = list(url_path['0'])
base_dir = './prodcast.clearhq.org'


for i in url_list:
    title1 = ''
    transcript = ''
    audio_path = ''
    audio = ''
    try:
        print(i)
        driver.get(i)
        time.sleep(10)
        title1 = driver.find_element_by_xpath('//div[@class="posttitle"]/h1')
        title1 = title1.text
        print(title1)
        try:
            transcript_pdf = driver.find_element_by_xpath('//div[@class="entry"]/p[2]')
            transcript_pdf= transcript_pdf.text
            print(transcript_pdf)
            urls = re.findall('(https?://\S+)', transcript_pdf)
            print(urls)
            transcript_pdf=urls[0]
            transcript_pdf=transcript_pdf.replace(")","")
            # print("transcript_pdf",transcript_pdf)
            transcript_pdf2 = driver.find_element_by_xpath('//div[@class="entry"]/p[3]')
            transcript_pdf2= transcript_pdf2.text
            transcript_pdf2=transcript_pdf2.replace ('\n', '')
            urls2 = re.findall('(https?://\S+)', transcript_pdf2)
            transcript_pdf2 = urls2[0]
            transcript_pdf2 = transcript_pdf2.replace(")", "")
            print("transcript_pdf", transcript_pdf2)
        except:
            print("Need to change xpath of transcript")
            pass

        try:
            try:
                title2 = driver.find_element_by_xpath('//div[@class="entry"]/p[1]')
                title = title1 + os.linesep + title2.text
            except:
                title = title1
            file_name = title1.replace(" ", "_")
            audio = driver.find_element_by_xpath('//div[@class="pbplayerBox theme9"]')
            print(audio, 'data')
            link = audio.get_attribute('data-uri')
            print(link, "audio_link")
            text = "audio_file"
            params = {
                "ie": "UTF-8",
                "client": "tw-ob",
                "q": text,
                "tl": "en",
                "total": "1",
                "idx": "0",
                "textlen": str(len(text))
            }
            response = requests.get(link, params=params)
            response.raise_for_status()

            assert response.headers["Content-Type"] == "audio/mpeg"
            with open("output.mp3", "wb") as file:
                file.write(response.content)
            print("Done.")

            os.rename("output.mp3", file_name + ".mp3")
            path = os.path.join(base_dir, file_name)
            os.mkdir(path)
            driver.get(transcript_pdf)
            time.sleep(4)
            try:
                if driver.find_element_by_xpath('//div[@class="mc-closeModal"]'):
                    driver.find_element_by_xpath('//div[@class="mc-closeModal"]').click()
                else:
                    pass
            except:
                print('+++')
                pass

            try:
                date_ = driver.find_element_by_xpath('//*[@id="id_aN5MTyM"]/div/p[1]')
                date_ = date_.text
                print(date_)
                post_date = datetime.strptime(date_, "%B %d, %Y").strftime("%m/%d/%Y")
                print(post_date, "post_date")
            except:
                date_ = driver.find_element_by_xpath('//*[@id="id_aN5MTyM"]/div/div[3]/p[2]')

                date_ = date_.text
                print(date_)
                post_date = datetime.strptime(date_, "%B %d, %Y").strftime("%m/%d/%Y")
                print(post_date, "post_date")
            transcript=''
            print("getting pdf from",transcript_pdf2)
            urllib.request.urlretrieve(transcript_pdf2,'transcript.pdf')
            pdfFileObj = open('transcript.pdf', 'rb')
            def convert_pdf_to_string(file_path):

                output_string = StringIO()
                with open(file_path, 'rb') as in_file:
                    parser = PDFParser(in_file)
                    doc = PDFDocument(parser)
                    rsrcmgr = PDFResourceManager()
                    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                    interpreter = PDFPageInterpreter(rsrcmgr, device)
                    for page in PDFPage.create_pages(doc):
                        interpreter.process_page(page)

                return (output_string.getvalue())


            transcript=convert_pdf_to_string('./transcript.pdf')
            print(transcript,"..........")
            if os.path.exists("./transcript.pdf"):
                os.remove("./transcript.pdf")
            with open(file_name + '_orig.txt', 'w') as f:
                for line in transcript:
                    f.write(line)
            with open(file_name + '.txt', 'w') as f:
                for line in title:
                    f.write(line)
            with open(file_name + '_info.txt', 'w') as f:
                f.write(i + '\n')
                f.write(post_date)
            print("Scraped transcript data")

            shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
            print('audio moved successful')
            shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
            shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
            shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
            print('All done..')
        except Exception as e:
            print(e)
            if os.path.exists("./output.mp3"):
                os.remove("./output.mp3")
            pass
    except:
        print("++++++++++++++++++")
        pass

import pandas as pd
from selenium import webdriver
import time


driver = webdriver.Chrome('./chromedriver')
sportsbook_url = "https://sportsbook.fanduel.com/"
match_urls=[]
data_final=[]
try:
    driver.maximize_window()
    driver.get(sportsbook_url)
    time.sleep(10)
    try:
        mlb = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div/div[1]/div/div/a[6]')

        link = mlb.get_attribute('href')
        driver.get(link)
        time.sleep(3)
        data = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/div[3]/div')
        mlb = data.find_elements_by_tag_name('a')
        for x in mlb:
            Mlb_match=x.get_attribute('href')
            print(Mlb_match)
            match_urls.append(Mlb_match)
        print(len(match_urls))
        match_list=list(set(match_urls))
        print(len(match_list))
        data_list=[]
        for i in match_list:
            print(i)
            driver.get(i)
            time.sleep(6)
            if True:
                try:
                    print("11")
                    aa=driver.find_element_by_xpath('//div[@class="t u v w by bz x if dp h fr fs"]')
                    print(aa.text)
                    data_1 = aa.text
                    with open('data.txt', 'w') as f:
                        for line in data_1:
                            f.write(line)

                except:
                    print("type2")
                    aa = driver.find_element_by_xpath('//div[@class="t u v w by bz x ij dp h fr fs"]')
                    print(aa.text)
                    data_1=aa.text
                    lines = []
                    with open('data.txt', 'w') as f:
                        for line in data_1:
                            f.write(line)
            else:

                try:
                    print("type3")
                    aa = driver.find_element_by_xpath('//div[@class="t u v w by bz x ip dp h fr fs"]')
                    print(aa.text)
                    data_1 = aa.text
                    lines = []
                    with open('data.txt', 'w') as f:
                        for line in data_1:
                            f.write(line)
                except Exception as e:
                    pass

            with open("data.txt") as file_in:
                lines = []
                for line in file_in:
                    lines.append(line.replace("\n", ""))
            print(lines)
            try:
                if len(lines)>=13:
                    home_team=lines[0]+ "(" + lines[1] +")"
                    print(home_team)
                    away_team=lines[2]+ "(" + lines[3] +")"
                    print(away_team)
                    home_spred=lines[4]+ "(" + lines[5] +")"
                    home_money=lines[6]
                    home_Total=lines[7]
                    away_spred=lines[8]+ "(" + lines[9] +")"
                    away_money=lines[10]
                    away_total=lines[11]
                    final_list = []
                    final_list.append(home_team)
                    final_list.append(away_team)
                    final_list.append(home_spred)
                    final_list.append(away_spred)
                    final_list.append(home_money)
                    final_list.append(away_money)
                    final_list.append(home_Total)
                    final_list.append(away_total)
                elif len(lines)<=4:
                    try:
                        home_team = lines[0]
                    except:
                        pass
                    try:
                        away_team = lines[1]
                    except:
                        pass
                    try:
                        home_money = lines[3]
                    except:
                        pass
                    try:
                        away_money = lines[4]
                    except:
                        pass
                    final_list=[]
                    final_list.append(home_team)
                    final_list.append(away_team)
                    final_list.append(None)
                    final_list.append(None)
                    final_list.append(home_money)
                    final_list.append(away_money)
                    final_list.append(None)
                    final_list.append(None)
                elif len(lines)<=2:
                    try:
                        home_team = lines[0]
                    except:
                        pass
                    try:
                        away_team = lines[1]
                    except:
                        pass
                    try:
                        home_money = lines[3]
                    except:
                        pass
                    try:
                        away_money = lines[4]
                    except:
                        pass
                    final_list=[]
                    final_list.append(home_team)
                    final_list.append(away_team)
                    final_list.append(None)
                    final_list.append(None)
                    final_list.append(None)
                    final_list.append(None)
                    final_list.append(None)
                    final_list.append(None)
                elif len(lines)>=10:
                    home_team = lines[0]
                    print(home_team)
                    away_team = lines[1]
                    print(away_team)
                    home_spred = lines[2] + "(" + lines[3] + ")"
                    home_money = lines[4]
                    home_Total = lines[5]
                    away_spred = lines[6] + "(" + lines[7] + ")"
                    away_money = lines[8]
                    away_total = lines[9]
                    final_list=[]
                    final_list.append(home_team)
                    final_list.append(away_team)
                    final_list.append(home_spred)
                    final_list.append(away_spred)
                    final_list.append(home_money)
                    final_list.append(away_money)
                    final_list.append(home_Total)
                    final_list.append(away_total)

                else:
                    print("No data found")
                    pass
                final_list.append()
            except Exception as e:
                print(e)
                pass
            title=["Home_team","Away_team","home_spread","away_spread","home_money","away_money","home_total","away_total"]
            data_final.append(title)
            data_final.append(final_list)

        time.sleep(10)

    except Exception as e:
        print(e)
        pass
except:
    print("!!!!!!!!!!!!!!!!!!")
    pass
df = pd.DataFrame(data_final)
df.to_csv('MLB_data2.csv',index=False)

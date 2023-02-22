# WebScraping (podcast data>> audio & transcript)
This file contain automation script that will scrape the podcast data(70+ podcast website) including tilte, podcast URL audio(tilte.mp3/wav) and transcript and store it in a spacific file structure. 
Website Name is same as folder name( like floder name: 17_governmentdigitalservice.podbean, website:https://governmentdigitalservice.podbean.com/)


The Selenium lib have some update in new Selenium2 so there will be some changes like:


selenium >> driver.find_element_by_xpath("xpath")


selenium2 >> driver.find_element(By.XPATH, "xpath")


so make changes accoring this>>
#### find_element(By.ID, "id")
#### find_element(By.NAME, "name")
#### find_element(By.XPATH, "xpath")
#### find_element(By.LINK_TEXT, "link text")
#### find_element(By.PARTIAL_LINK_TEXT, "partial link text")
#### find_element(By.TAG_NAME, "tag name")
#### find_element(By.CLASS_NAME, "class name")
#### find_element(By.CSS_SELECTOR, "css selector")

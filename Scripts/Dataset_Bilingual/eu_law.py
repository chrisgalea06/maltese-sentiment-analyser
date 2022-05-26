from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime

def save_list(list, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in list:
            f.write(str(item)+'\n')


start_time = datetime.now()
print(start_time)

print('Started...')
service = Service("executables\chromedriver.exe")
browser = webdriver.Chrome(service=service)
unwanted_words = ['article','section','chapter','type','annex']
laws = []
for count in range(300,10000):
    url = "https://eur-lex.europa.eu/search.html?SUBDOM_INIT=ALL_ALL&DTS_SUBDOM=ALL_ALL&DTS_DOM=ALL&type=advanced&lang=en&qid=1639754468947&page="+str(count)
    browser.get(url)
    #time.sleep(2)
    english_laws = []
    maltese_laws = []

    for i in range(6,16):
        new_url ='//div['+str(i)+']//h2[1]//a[1]'
        browser.find_element(By.XPATH,new_url).click()
        time.sleep(2)

        english_url  = browser.current_url
        maltese_url = english_url.replace("EN","MT",1)
        for element in browser.find_elements(By.TAG_NAME,'td'):
            english_laws.append(element.text)
        browser.get(maltese_url)

        for element in browser.find_elements(By.TAG_NAME,'td'):
            maltese_laws.append(element.text)

        is_index = False
        for law_1,law_2 in zip(english_laws,maltese_laws):
            if is_index:
                if len(law_1) <5:
                    is_index = False
                    continue
                if len(law_1.split(' ')) <3:
                    is_index = False
                    continue
                if any(word in law_1.lower() for word in unwanted_words):
                    is_index = False
                    continue
                if sum(c.isdigit() for c in law_1) > 3:
                    is_index = False
                    continue
                laws.append((law_1.strip(),law_2.strip()))
                is_index = False
            if(law_1 == law_2):
                is_index = True
                
        save_list(laws,'Output Files/laws3.txt')
        browser.get(url)

browser.close()
print('Finished running...')
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
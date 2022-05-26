from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime


# Keeping track of running time
start_time = datetime.now()
print(start_time)


print('Started...')


service = Service("executables\chromedriver.exe")
browser = webdriver.Chrome(service=service)

browser.get("https://malti.global.bible/bible/2cd26dfc051b0283-01/GEN.1")
browser.maximize_window()
time.sleep(5)

element = browser.find_element(
    By.XPATH, "//body/div[@id='root']/section[@class='sc-AxhCb sc-qXhiz eVSRgY']/div/div[@class='sc-AxirZ exnRXS']/div/div[@class='sc-fzoxKX sc-pIJJz fvNxrc']/div[@class='sc-fzoKki sc-pRFjI kyMqDT']/div[2]/div[1]/div[1]/div[1]")
element.click()


element = browser.find_element(
    By.XPATH, "//div[@class='sc-fznBMq ekttti']/child::div")
element.click()


div_elements = element.find_elements(
    By.XPATH, "//div[@class='sc-fznBMq ekttti']/child::div")

div_ids = []
for e in div_elements:
    div_ids.append(e.get_attribute('id'))

bible_structure = {}


for i in range(len(div_ids)):
    id = div_ids[i]
    path = "//div[@id='"+str(id)+"']"

    element = browser.find_element(By.XPATH, path)
    element.click()

    child_path = "//div[@class='sc-fznBMq ekttti']/child::div"
    child_elements = element.find_elements(By.XPATH, str(child_path))
    chapter_id = child_elements[i+1].get_attribute('class')

    chapter_path = "//div[@class='"+str(chapter_id)+"']/child::div"
    books_elements = child_elements[i +
                                       1].find_elements(By.XPATH, str(chapter_path))

    list_of_books = []
    for j in range(len(books_elements)):
        ce = books_elements[j]
        
        if ce.text.isnumeric():
            # list_of_books.append((j, ce.get_attribute('class')))
            list_of_books.append(j)
          
    bible_structure[id] = list_of_books


with open('bible_books.json', 'w', encoding='utf-8') as fp:
    json.dump(bible_structure, fp,  indent=4)


browser.close()

print('finished running...')
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

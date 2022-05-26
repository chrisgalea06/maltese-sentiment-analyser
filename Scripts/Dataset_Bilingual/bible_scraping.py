from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime


def export_to_json(dict, filename):
    with open(filename, 'w', encoding='utf-8') as fp:
        json.dump(dict, fp,  indent=4, ensure_ascii=False)

    return


def get_title_maltese():
    text = browser.find_element(By.XPATH, "/html/body").text
    lines = text.splitlines()
    return lines[0]


def extract_text_maltese():
    element = browser.find_element(
        By.XPATH, "//div[@id='current-chapter-col']")
    child_elements = element.find_elements(By.TAG_NAME, "span")
    text = ''
    for child in child_elements:
        if child.text != '':
            text = text + child.text + '\n'
    return text


def parse_text_maltese(text):
    chapter_content = []
    lines = text.splitlines()
    current = ''
    count = 0
    for line in lines:
        if line.isnumeric():
            if count > 0:
                chapter_content.append((count, current))
                current = ''
            count += 1
        else:
            current = current + ' ' + line
    chapter_content.append((count, current))

    return chapter_content


def scrape_maltese_bible(browser):
    browser.get("https://malti.global.bible/bible/2cd26dfc051b0283-01/JUD.1")
    #browser.minimize_window()
    time.sleep(5)
    bible = {}

    with open('Output Files/bible_maltese.json',encoding='utf8') as json_file:
        bible = json.load(json_file)

    while True:

        if not '.intro' in browser.current_url:            
            text = extract_text_maltese()
            title = get_title_maltese()
            chapter_content = parse_text_maltese(text)

            bible[title] = chapter_content
        if(browser.current_url == 'https://malti.global.bible/bible/2cd26dfc051b0283-01/JUD.1'):
            break
        element = browser.find_element(
            By.XPATH, "//body/div[@id='root']/section[@class='sc-AxhCb sc-qXhiz eVSRgY']/div[@class='sc-oTmZL kBRbXj']/div[3]")
        element.click()

    browser.close()

    export_to_json(bible, 'Output Files/bible_maltese.json')

    return


def get_title_english():
    title = browser.title
    tokens = title.split(' - ')

    return tokens[0] + ' ' + tokens[1].replace("Chapter ", "")


def extract_text_english():
    element = browser.find_element(
        By.XPATH, "//div[@id='bibleBook']")
    child_elements = element.find_elements(By.TAG_NAME, "p")
    text = ''
    for child in child_elements:
        if child.text != '':
            text = text + child.text + '\n'
    return text


def parse_text_english(text):
    chapter_content = []
    lines = text.splitlines()
    for line in lines:
        verse_no = ''
        verse = line
        if(len(line) == 1 or len(line) == 2):
            verse_no = line
        elif(len(line)>0):
            for i in range(0, 2):
                char = line[i]
                if char.isnumeric():
                    verse_no += char
        if verse_no != '':
            verse = verse.replace(verse_no+' ', "")
            chapter_content.append((int(verse_no), verse))
    return chapter_content


def scrape_english_bible(browser):
    total_bible_books = 73
    bible = {}
    for i in range(1, total_bible_books+1):
        count = 1
        max_count = 0
        while True:
            if count == 1:
                url = "https://www.catholic.org/bible/book.php?id="+str(i)
                browser.get(url)
                browser.minimize_window()
                element = browser.find_element(
                    By.XPATH, "(//ul[@class='pagination Chapters'])[1]")
                child_elements = element.find_elements(By.TAG_NAME, "li")
                max_count = len(child_elements)-2
                title = get_title_english()
                text = extract_text_english()
                chapter_content = parse_text_english(text)
                bible[title] = chapter_content
                count += 1
            elif count > max_count:
                break
            else:
                url = "https://www.catholic.org/bible/book.php?id=" + \
                    str(i)+"&bible_chapter="+str(count)
                browser.get(url)
                browser.minimize_window()
                title = get_title_english()
                text = extract_text_english()
                chapter_content = parse_text_english(text)
                bible[title] = chapter_content
                count += 1
    browser.close()

    export_to_json(bible, 'Output Files/bible_english.json')
    return


if __name__ == '__main__':
    # Keeping track of running time
    start_time = datetime.now()
    print(start_time)

    print('Started...')
    service = Service("executables\chromedriver.exe")
    browser = webdriver.Chrome(service=service)
    scrape_maltese_bible(browser)
    #scrape_english_bible(browser)

    print('Finished running...')
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

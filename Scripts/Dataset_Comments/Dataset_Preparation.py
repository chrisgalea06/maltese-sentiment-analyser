# Import required libraries
import pandas as pd
import os
import re
import langid
import string
import numpy as np
import json
import requests
# import nltk
from datetime import datetime
import random

def save_list(list, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in list:
            f.write("%s, " % item)

    #print('\nSaved successfully to ', filename)
    return


def open_list(filename):
    with open(filename, "r", encoding='utf-8') as f:
        mylist = f.readlines()

    word_list = []
    for line in mylist:
        if word_list:
            word_list.extend(line.split(", "))
        else:
            word_list = line.split(", ")

    return word_list


def clean_word(word):
    word = re.sub(r'[^\w\s]', '', word)
    word = word.lower()

    return word


def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))


def clean_list(list):
    new_list = []
    for word in list:
        new_word = clean_word(word)
        new_list.append(new_word)
    return new_list


def tokenize(text):
    words = WORD.findall(text)
    return words


def check_list(list, word):
    if word in list:
        return True
    else:
        return False

        # https://stackoverflow.com/a/49146722/330558


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


if __name__ == '__main__':
    #nltk.download('punkt')

    # # Keeping track of running time
    # start_time = datetime.now()
    # print(start_time)

    # WORD = re.compile(r'\w+')

    # print('Started...')

    # # ---------- Part 1: Reading comments from csv files and removing any unneccesary comments ----------
    # print('Generating filenames...\n')
    # filenames = next(os.walk('Comments/'),
    #                  (None, None, []))[2]  # [] if no file
    # print(filenames)

    # print('\nReading each csv file to a dataframe...')
    # dataframes = []
    # for f in filenames:
    #     df = pd.read_csv("Comments/"+f)
    #     df = df['message']
    #     dataframes.append(df)
    #     break

    # print(len(dataframes), ', CSV files found')

    # print('\nConverting each dataframe to list...')

    # comments_v1 = []
    # for df in dataframes:
    #     temp_comments = df.to_numpy().tolist()
    #     if comments_v1:
    #         comments_v1.extend(temp_comments)
    #     else:
    #         comments_v1 = temp_comments

    # print(len(comments_v1),', Comments found')
    # #print(comments_v1[0:10])

    # print('\nChecking whether each comment is a sentence long...')

    # comments_v2 = []
    # for comment in comments_v1:
    #     comment = str(comment).strip()
    #     a_list = nltk.tokenize.sent_tokenize(comment)
    #     if comments_v2:
    #         comments_v2.extend(a_list)
    #     else:
    #         comments_v2 = a_list

    # print(len(comments_v2),', Comments generated')
    # #print(comments_v2[0:10])

    # # Most comments extracted from these pages have multiple comments which are repetitive or have words which are in english
    # # Hence a list with these sample words was generated in order to remove such comments

    # print('\nRemoving unwanted comments...')
    # common_words = ['nan','Goodluck','Good luck','Good Luck','GoodLuck','Welldone', 'Well done','RIP','rip','proud'
    #                ,'Proud','well','done','Rip','Bravu','proset','Bravi','Brava','God','Grazzi','Thank']

    # common_words_re = re.compile("|".join(common_words))

    # comments_v3 = []

    # for comment in comments_v2:

    #     comment = str(comment).strip()
    #     if common_words_re.search(comment):
    #         continue
    #     else:
    #         comment = remove_emoji(comment)
    #         comments_v3.append(comment)

    # print(len(comments_v3),', Comments generated')
    # #print(comments_v3[0:10])

    # print('\nRemoving more unwanted comments...')

    # comments_v4 = []
    # for comment in comments_v3:
    #     if len(comment)>2:
    #         comments_v4.append(comment)

    # print(len(comments_v4),', Comments generated')
    # #print(comments_v4[0:10])

    # print('\nRemoving comments written in English...')
    # final_comments = []
    # for comment in comments_v4:
    #     lang = langid.classify(comment)
    #     if lang[0] != 'en':
    #         final_comments.append(comment)

    # save_list(final_comments,'Output Files/final_comments.txt')


    # ---------- Part 2: Building the Maltese Lexicon ----------
    # print('Generating maltese lexicon...')
    # print('Reading first .json file...')

    # data = []
    # for line in open('Resources/maltese_words.json', 'r', encoding='utf-8'):
    #     data.append(json.loads(line))

    # print('Reading second .json file...')

    # for line in open('Resources/other_maltese_words.json', 'r', encoding='utf-8'):
    #     data.append(json.loads(line))


    # print('Extracting maltese words...')

    # lexemes = []
    # for d in data:
    #     if 'lemma' in d:
    #         lemma = clean_word(d['lemma'])
    #         if len(lemma) > 1:
    #             lexemes.append(lemma)
    #     if "surface_form" in d:
    #         lexemes.append(d['surface_form'])
    #     if "plural_form" in d:
    #         lexemes.append(d['plural_form'])
    #     if "alternatives" in d:
    #         lexemes.append(d['alternatives'])

    # print('Formatting list of maltese words...')

    # maltese_words = []
    # for word in lexemes:
    #     if type(word) != str:
    #         maltese_words.extend(word)
    #     elif ' ' in word:
    #         words = tokenize(word)
    #         maltese_words.extend(words)
    #     else:
    #         maltese_words.append(word)

    # maltese_words = list(filter(lambda a: a != '', maltese_words))

    # print(len(maltese_words),', Maltese words generated')

    # print('Removing unwanted words...')

    # special_characters = "_пc*"

    # final_maltese_words = []

    # for word in maltese_words:
    #     if not has_numbers(word) and not any(c in special_characters for c in word):
    #         final_maltese_words.append(word.lower())

    # print('Saving to file...')
    # save_list(final_maltese_words,'Output Files/maltese_words.txt')

    # ---------- Part 3: Using Lexicon to determine which comments have any misspelled words ----------

    # maltese_words = open_list('Output Files/maltese_words.txt')
    # print('Number of final comments ',len(maltese_words))

    # final_comments = open_list('Output Files/final_comments.txt')
    # print('Number of final comments ',len(final_comments))

    # print('Placing maltese words in a dictionary...')
    # dict_of_maltese_words = {}
    # for word in maltese_words:
    #     temp_list = []
    #     if len(word)>1:
    #         if word[0] in dict_of_maltese_words.keys():
    #             temp_list = dict_of_maltese_words[word[0]]
    #             temp_list.append(word)
    #             dict_of_maltese_words[word[0]] = temp_list
    #         else:
    #             temp_list.append(word)
    #             dict_of_maltese_words[word[0]] = temp_list


    # print('Checking comments for any misspelled word...')

    # incorrect_words = []

    # for sentence in final_comments:
    #     sent = tokenize(sentence)
    #     for word in sent:
    #         if not word.isdigit():
    #             word = clean_word(word)
    #             if not check_list(incorrect_words,word):
    #                 if word[0] in dict_of_maltese_words.keys():
    #                     if not check_list(dict_of_maltese_words[word[0]],word):
    #                         incorrect_words.append(word)

    # save_list(incorrect_words,'Output Files/misspelled_words_v1.txt')

    # ---------- Part 4: Generating suggestions of misspelled words through API ----------
    # misspelled_words = open_list('Output Files/misspelled_words_v1.txt')
    # print(len(misspelled_words))

    # final_comments = open_list('Output Files/final_comments.txt')
    # print('Number of final comments ',len(final_comments))

    # print('Generating suggestions of misspelled words through API...')
    # word_suggestions = {}

    # for word in misspelled_words:
    #     r = requests.get(' https://mlrs.research.um.edu.mt/resources/gabra-api/lexemes/search_suggest?s='+word)
    #     if(r.json()['results']):
    #         result = r.json()['results'][0]['lexeme']['lemma']
    #         word_suggestions[word] = result
    #         misspelled_words.remove(word)

    # print('Suggestions generated: ',len(word_suggestions))

    # save_list(misspelled_words,'Output Files/misspelled_words_v2.txt')

    # with open('Output Files/suggestions_v1.json', 'w',encoding='utf-8') as fp:
    #     json.dump(word_suggestions, fp,  indent=4)

    # # Opening JSON file
    # f = open('Output Files/suggestions.json', encoding='utf-8')

    # # returns JSON object as
    # # a dictionary
    # data = json.load(f)

    # # Iterating through the json
    # # list
    # word_suggestions = {}
    # for i in data:
    #     word_suggestions[i] = data[i]

    # # Closing file
    # f.close()

    # final_comments = open_list('Output Files/final_comments.txt')
    # print('Number of final comments ',len(final_comments))

    # final_comments_v2 = []
    # for comment in final_comments:
    #     comment = comment.lower()
    #     final_comments_v2.append(comment)

    # save_list(final_comments_v2,'Output Files/final_comments_v2.txt')

    # ---------- Part 6: Substituting word suggestions with misspelled words ----------

    # for word in word_suggestions:
    #     final_comments_v2 = open_list('Output Files/final_comments_v2.txt')
    #     final_comments_v2 = [sub.replace(word, word_suggestions[word]) for sub in final_comments_v2]
    #     save_list(final_comments_v2,'Output Files/final_comments_v2.txt')


    # final_comments_v2 = open_list('Output Files/final_comments_v2.txt')
    # print('Number of final comments ',len(final_comments_v2))

    # final_comments_v3 = []
    # for comment in final_comments_v2:
    #     comment = comment.capitalize()
    #     final_comments_v3.append(comment)

    # save_list(final_comments_v3,'Output Files/final_comments_v3.txt')

    # final_comments_v4 = open_list('Output Files/final_comments.txt')
    # random.shuffle(final_comments_v4)

    # indexes = list(range(0, len(final_comments_v4)))

    # df = pd.DataFrame(final_comments_v4, columns =['message'])
    # df['index'] = indexes
    # df['annotation1'] = ""
    # df['annotation2'] = ""
    # df['annotation3'] = ""

    # print(df.head())


    # df.to_csv('Output Files/database.csv', encoding='utf-8',index=False)

    # end_time = datetime.now()
    # print('Duration: {}'.format(end_time - start_time))
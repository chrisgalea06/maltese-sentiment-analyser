from google.cloud import language
import os
import pandas as pd
import requests
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import json
from nltk.tokenize import sent_tokenize
import langid

def open_list(filename):
    with open(filename, "r", encoding='utf-8') as f:
        mylist = f.readlines()

    return mylist

def export_to_json(dict, filename):
    with open(filename, 'w', encoding='utf-8') as fp:
        json.dump(dict, fp,  indent=4, ensure_ascii=False)

    return


def open_json(filename):
    f = open(filename, encoding='utf-8')
    return json.load(f)


def google_analyze_sentiment(text):

    client = language.LanguageServiceClient()
    type_ = language.Document.Type.PLAIN_TEXT

    lan = "en"
    document = {"content": text, "type_": type_, "language": lan}
    encoding_type = language.EncodingType.UTF8

    response = client.analyze_sentiment(
        request={'document': document, 'encoding_type': encoding_type})

    score = response.document_sentiment.score

    if score <= 1 and score >= (1-(2/3)):
        return 'positive'
    elif score >= -1 and score <= (-1+(2/3)):
        return 'negative'
    else:
        return 'neutral'


def textprocess_analyze_sentiment(text):
    data = {
        'text': text
    }
    response = requests.post(
        'http://text-processing.com/api/sentiment/', data=data)
    if response.json()['label'] == 'pos':
        return 'positive'
    elif response.json()['label'] == 'neg':
        return 'negative'
    elif response.json()['label'] == 'neutral':
        return 'neutral'
    else:
        return 'no-sentiment'


def microsoft_analyze_sentiment(text):
    credential = AzureKeyCredential("f5c3bc0461ee4a0ba60d6c37d9cef82a")
    text_analytics_client = TextAnalyticsClient(
        endpoint="https://sentanalysis1234.cognitiveservices.azure.com/", credential=credential)
    response = text_analytics_client.analyze_sentiment(text)
    successful_responses = [doc for doc in response if not doc.is_error]
    if successful_responses:
        return successful_responses[0].sentiment
    else:
        return 'no-sentiment'


if __name__ == "__main__":
    print('Started running...')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"Keys\NLP.json"

    laws = open_list('Output Files/laws.txt')
    # laws.extend(open_list('Output Files/laws.txt'))
    maltese_laws = []
    english_laws = []
    for line in laws:
        law = line.split('\', \'')
        if len(law) == 1:
            law = line.split('\', \"')
        if len(law) == 1:
            law = line.split('\", \'')  
        if len(law) == 1:
            law = line.split('\", \"') 
        maltese_laws.append(law[1][:len(law[1]) - 3])
        english_laws.append(law[0][2:])

    # clean_maltese_laws = []
    # clean_english_laws = []
    # for malt_law,engl_law in zip(maltese_laws,english_laws):
    #     maltese = sent_tokenize(malt_law)
    #     english = sent_tokenize(engl_law)
    #     if clean_maltese_laws:
    #         clean_maltese_laws.extend(maltese)
    #     else:
    #         clean_maltese_laws= maltese

    #     if clean_english_laws:
    #         clean_english_laws.extend(english)
    #     else:
    #         clean_english_laws= english

    print('Starting sentiment generation...')
    df= pd.read_csv('Output Files/law_sentiment.csv')
    parsed_laws = df['comment'].tolist()
    for malt_law,engl_law in zip(maltese_laws,english_laws):
        
        if not malt_law in parsed_laws:
            # print(malt_law)
            # print()

            # print(engl_law)

            sentiment_1 = textprocess_analyze_sentiment(engl_law)
            sentiment_2 = microsoft_analyze_sentiment([str(engl_law)])
            # print(sentiment_2)

            sentiment_3 = google_analyze_sentiment(engl_law)
            # print(sentiment_3)

            parsed_laws.append(malt_law)

            df_comment = {"comment":malt_law, "sentiment 1":sentiment_1,"sentiment 2":sentiment_2,"sentiment 3":sentiment_3}
            df = df.append(df_comment, ignore_index = True)
            df.to_csv('Output Files/law_sentiment.csv', encoding='utf-8',index=False)
            df_parsed = pd.DataFrame(parsed_laws, columns =['comment'])
            df_parsed.to_csv('Output Files/parsed laws.csv', encoding='utf-8',index=False)
       
        
    

    # maltese_bible = open_json('Output Files/bible_maltese.json')
    # english_bible = open_json('Output Files/bible_english.json')

    # maltese_books = [*maltese_bible]
    # english_books = [*english_bible]
    # titles_translations = [('LEVITIKU', 'Leviticus'), ('DEWTERONOMJU', 'Deuteronomy'), ('SOFONIJA', 'Zephaniah'), ('LUQA', 'Luke'), ('1 SLATEN', '1 Kings'), ('2 SLATEN', '2 Kings'),
    #                        ('LHUD', 'Hebrews'), ('SALMI', 'Psalms'), ('MĦALLFIN', 'Judges'), ('1 SAMWEL', '1 Samuel'), ('2 SAMWEL','2 Samuel'), ('EFESIN', 'Ephesians'), ('FILEMON', 'Philemon'), ('MARK', 'Mark'), ('NEĦEMIJA', 'Nehemiah'),
    #                        ('ATTI TAL-APPOSTLI', 'Acts of Apostles'), ('ESDRA','Ezra'), ('ĦAGGAJ', 'Haggai'),('DANJEL BIL-GRIEG', 'Daniel'), ('1 KRONAKI', '1 Chronicles'), ('2 KRONAKI','2 Chronicles'), ('GĦABDIJA', 'Obadiah'), ('ĠEREMIJA', 'Jeremiah'),
    #                        ('MALAKIJA', 'Malachi'), ('GALATIN', 'Galatians'),('MATTEW', 'Matthew'),('1 ĠWANNI', '1 John'), ('RUT', 'Ruth'), ('NAĦUM', 'Nahum'), ('2 ĠWANNI', '2 John'), ('3 ĠWANNI', '3 John'),
    #                        ('L-GĦANJA TAL-GĦANJIET', 'The Song of Songs'),('ĠUDITTA', 'Judith'), ('APOKALISSI', 'Revelation'), ('ĠOEL', 'Joel'), ('ĠONA','Jonah'), ('ĠAKBU', 'James'), ('EŻEKJEL', 'Ezekiel'), ('FILIPPIN', 'Philippians'),
    #                        ('1 TESSALONIKIN', '1 Thessalonians'), ('2 TESSALONIKIN','2 Thessalonians'),('LAMENTAZZJONIJIET', 'Lamentations'), ('MIKEA','Micah'), ('KOĦÈLET', 'Ecclesiastes'), ('PROVERBJI', 'The Proverbs'),
    #                        ('GĦAMOS', 'Amos'), ('ĠOŻWÈ', 'Joshua'), ('BIN SIRAK', 'Ecclesiasticus / Sirach'), ('ĦABAKKUK','Habakkuk'), ('1 MAKKABIN', '1 Maccabees'), ('2 MAKKABIN', '2 Maccabees'),
    #                        ('ŻAKKARIJA', 'Zechariah'), ('NUMRI', 'Numbers'),('HOSEGĦA', 'Hosea'), ('IL-KTIEB TAL-GĦERF','Wisdom'), ('1 PIETRU', '1 Peter'), ('2 PIETRU', '2 Peter'), ('KOLOSSIN', 'Colossians'),
    #                        ('ĠENESI', 'Genesis'), ('ĠOB', 'Job'),('EŻODU', 'Exodus'), ('1 KORINTIN', '1 Corinthians'), ('2 KORINTIN', '2 Corinthians'), ('ĠUDA', 'Jude'), ('ESTER BIL-GRIEG','Esther'), ('ISAIJA', 'Isaiah'), ('TOBIT', 'Tobit'), ('1 TIMOTJU', '1 Timothy'), ('2 TIMOTJU', '2 Timothy'),
    #                        ('RUMANI', 'Romans'),('TITU', 'Titus'), ('BÀRUK', 'Baruch')]

    # df= pd.read_csv('Output Files/bible_sentiment.csv')
    # parsed_comments = df['comment'].tolist()
    # for title in titles_translations:
    #     curr_books_maltese = [s for s in maltese_books if title[0] in s]
    #     curr_books_english = [s for s in english_books if title[1] in s]  
    #     for i in range(len(curr_books_maltese)):
    #         maltese_book = curr_books_maltese[i]
    #         english_book = curr_books_english[i]
    #         list_of_english_verses = english_bible[english_book]
    #         list_of_maltese_verses = maltese_bible[maltese_book]
    #         for j in range(len(list_of_english_verses)):
    #             if len(list_of_english_verses) == len(list_of_maltese_verses):
    #                 curr_malt_verse = list_of_maltese_verses[j]
    #                 if curr_malt_verse[1] in parsed_comments:
    #                     continue
    #                 if len(curr_malt_verse) > 3:
    #                     curr_english_verse = list_of_english_verses[j]
    #                     print(curr_malt_verse)
    #                     sentiment_1 = textprocess_analyze_sentiment(curr_english_verse[1])
    #                     sentiment_2 = microsoft_analyze_sentiment([curr_english_verse[1]])
    #                     sentiment_3 = google_analyze_sentiment(curr_english_verse[1])
    #                     parsed_comments.append(curr_malt_verse)
                        
    #                     df_comment = {"comment":curr_malt_verse[1], "sentiment 1":sentiment_1,"sentiment 2":sentiment_2,"sentiment 3":sentiment_3}
    #                     df = df.append(df_comment, ignore_index = True)
    #                     df.to_csv('Output Files/bible_sentiment.csv', encoding='utf-8',index=False)
    #                 else:
    #                     parsed_comments.append(curr_malt_verse)

                
            
    
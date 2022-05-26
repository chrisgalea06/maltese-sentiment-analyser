import os
import pandas as pd
from datetime import datetime
import six
from google.cloud import translate_v2 as translate
from azure.core.credentials import AzureKeyCredential
from sklearn.utils import shuffle


def translate_text(target, text):
    
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    print(u"Text: {}".format(result["input"]))
    
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

start_time = datetime.now()
print(start_time)

print('Started...')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"Keys\Translate_2.json"
translate_client = translate.Client()

df_tweets = pd.read_csv('Datasets/sentiment140.csv',header=None,names=['polarity', 'index','date','other','user','text'])
df_tweets = shuffle(df_tweets)
comments = df_tweets['text'].tolist()
polarity = df_tweets['polarity'].tolist()
annotation = []
for anno in polarity:
    if anno == 0:
        annotation.append('negative')
    elif anno == 2:
        annotation.append('neutral')
    elif anno == 4:
        annotation.append('positive')

df_parsed = pd.read_csv('Output Files/sentiment140 Parsed Comments.csv')
parsed_comments = df_parsed['comment'].tolist()

df_translated = pd.read_csv('Output Files/sentiment140 Translated Comments.csv')
translated_comments = df_translated['comment'].tolist()
# translated_comments = []
# parsed_comments = []
for comment in comments:
    if comment in parsed_comments:
        continue
    if isinstance(comment, six.binary_type):
        comment = comment.decode("utf-8")


    result = translate_client.translate(comment, target_language='mt',format_='text')
    parsed_comments.append(comment)
    translated_comments.append(result["translatedText"])
    df_parsed = pd.DataFrame(parsed_comments, columns =['comment'])
    df_parsed.to_csv('Output Files/sentiment140 Parsed Comments.csv', encoding='utf-8',index=False)
    df_translated = pd.DataFrame(translated_comments, columns =['comment'])
    df_translated['sentiment'] = annotation[0:len(translated_comments)]
    df_translated.to_csv('Output Files/sentiment140 Translated Comments.csv', encoding='utf-8',index=False)



print('Finished running...')
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

import pandas as pd
from datetime import datetime
import json

def export_to_json(dict, filename):
    with open(filename, 'w', encoding='utf-8') as fp:
        json.dump(dict, fp,  indent=4, ensure_ascii=False)

    return


start_time = datetime.now()
print(start_time)

print('Started...')

df = pd.read_csv('Datasets/Annotated Comments.csv')


df = df.drop(columns=['index'])

comments = []
annotation = []
no_majority ={} 
to_delete = []


for i in range(len(df['message'].tolist())):
    anno_1 = df['annotation1'][i]
    anno_2 = df['annotation2'][i]
    anno_3 = df['annotation3'][i]
    curr_comment = df['message'][i]

    if anno_1== 'TO-DELETE'or anno_2== 'TO-DELETE' or anno_3 == 'TO-DELETE':
        to_delete.append(curr_comment)
    elif anno_1 == anno_2:
        comments.append(curr_comment)
        annotation.append(anno_1)
    elif anno_2 == anno_3:
        comments.append(curr_comment)
        annotation.append(anno_2)
    elif anno_1 == anno_3:
        comments.append(curr_comment)
        annotation.append(anno_1)
    else:
        no_majority[curr_comment] = [anno_1,anno_2,anno_3]
    
print('Annotated dataset details: ')
print('Comments: ',len(comments))
print('Annotations: ',len(annotation))
print()
print('Number of comments in which annotators did not agree: ',len(no_majority.keys()))
print()
print('Number of comments to delete: ',+len(to_delete))

print('Comments downloaded from db: ',len(df['message'].tolist()))
print('Comments parsed: ',len(comments)+len(no_majority.keys())+len(to_delete))

export_to_json(no_majority, 'Output Files/No majority in annotation.json')

print('Finished running...')
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
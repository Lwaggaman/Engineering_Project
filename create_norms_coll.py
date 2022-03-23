from pymongo import MongoClient, UpdateOne
import pandas as pd
from text_funcs import clean_id
from pprint import pprint


config = {
  'host': '54.241.98.140:27017',
  'username': 'app_user',
  'password': 'rechazo',
  'authSource': 'cc_db'
}
client = MongoClient(**config)
db = client.cc_db

### Previously gathered and processed data. Note: Does not contain signatures, those will be added on updates.
cols_info = ['url','name','_id','topic','commision']
conv_text = pd.read_csv('Data/conv_docs2.csv', index_col=0)
conv_info = pd.read_csv('Data/conv_info.csv', names=cols_info, index_col=0, skiprows=1)

# Prep and merge
conv_info._id = conv_info._id.apply(clean_id)
conv_info.iloc[279, -3] = '455-5'
conv_text.text = conv_text.text.str.replace(r'\n',r' ', regex=True)
conv_text.index = conv_text.index.str.replace(r'.pdf', r'', regex=True)
conv = conv_info.merge(conv_text, how='left', left_index=True, right_index=True)
conv_dict = conv.iloc[:,[2,1,3,4,5,0]].to_dict('records')

def insert_norms():
    print('Creating "norms" collection:')
    #global conv_dict
    res = db.norms.bulk_write(
        [UpdateOne({'_id':doc['_id']}, {'$set': doc}, upsert=True) for doc in conv_dict]
        )
    pprint(res.bulk_api_result)
    if res.modified_count == 0:
        print('Updated: No new documents')

insert_norms()

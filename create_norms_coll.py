from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
import pandas as pd
from text_funcs import clean_id
from pprint import pprint
from db_connection import setup_client
import logging


client = setup_client()
db = client.cc_db

logging.basicConfig(filename='norms.log',datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


def gather_data():
    """Gathers previously processed data and preps for db upsertion"""
    ###Note: Does not contain signatures, those will be added on updates.
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
    return conv_dict

def insert_norms(data_dict):
    print('Creating "norms" collection:')
    logging.info('Creating norms collection')
    #global conv_dict
    try: 
        res = db.norms.bulk_write(
            [UpdateOne({'_id':doc['_id']}, {'$set': doc}, upsert=True) for doc in data_dict]
            )
        #for upserted_id in res.upserted_ids:
        #    logging.info(f"{upserted_id} has updated text")
        for upserted in res.bulk_api_result['upserted']:
            logging.info(f"{upserted['_id']} has updated text")
        print(f'Updated: {res.upserted_count} new documents with text')
    except BulkWriteError as bwe:
        for upserted in bwe.details['upserted']:
            logging.info(f"{upserted['_id']} has updated text")
        for error in bwe.details['writeErrors']:
            logging.error(f"failed to insert {error['op']['_id']}:{error['errmsg']}")
        print(f"Updated:{bwe.details['nUpserted']} new documents with text")


def create_norms():
    existing_colls = db.list_collection_names()
    if 'norms' in existing_colls:
        nr_docs = db.norms.count_documents({'url':{'$exists':True}})
        #docs_wo_text = db.norms.count_documents({'url':{'$exists':True}, 'text':{'$exists':False}})
        print(f'Norms collection with {nr_docs} documents already exists.')
        #print(f'{docs_wo_text} of the documents were missing text.')
    else:
        print('Gathering data...')
        data_dict = gather_data()
        insert_norms(data_dict)

create_norms()
import pandas as pd
from text_funcs import clean_id
from pymongo import MongoClient, UpdateOne
from pprint import pprint
from db_connection import setup_client

client = setup_client()
db = client.cc_db

logging.basicConfig(filename='signatures.log',datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

def update_signatures():
    """The Governments' transparency site has a csv that contains the names 
    of the Assemblymembers presenting a Norm Proposal.
    They have ceased to update it so it does not cover all proposals.
    This function updates documents in the database and adds 6 new ones."""
    cols_new = ['name', '_id', 'topic', 'signatures', 'commision', 'url']
    update = (pd.read_csv('Data/TransparenciaActiva.csv', encoding = "ISO-8859-1", sep=';', names=cols_new,
                            skiprows=[0,14]))
    update._id = update._id.apply(clean_id)
    update = update.to_dict('records')
    
    #Add signature field to existing docs
    print('Updating signatures in Norm Proposals from "norms"')
    try:
        new_sig = db.norms.bulk_write(
            [UpdateOne({'_id': doc['_id'],'signatures': {'$exists': False}},{'$set': {'signatures':doc['signatures']}}) for doc in update]
            )
        logging.info(f'Signatures added to following docs: {new_sig.bulk_api_result["upserted"]}')
        print(f'Added signature to {new_sig.matched_count} documents in db')
    except BulkWriteError as bwe:
        logging.info(f'Signatures added to following docs: {bwe.details["upserted"]}')
        for error in bwe.details['writeErrors']:
            logging.error(f"Failed to add signature: {error['op']['_id']}:{error['errmsg']}")
        print('Check log: Encountered error when adding signatures to existing docs in db')


    #create entire doc if not exists in db 
    for doc in update:
        if not db.norms.find_one({'_id':doc['_id']}):
            db.norms.insert_one(doc)
            logging.info(f'New doc "{doc['_id']}" was added to db')
    pprint(new_sig.bulk_api_result)
    if new_sig.modified_count == 0:
        print('Updated: No new documents')

update_signatures()


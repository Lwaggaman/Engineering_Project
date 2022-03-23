import pandas as pd
from text_funcs import clean_id
from pymongo import MongoClient, UpdateOne
from pprint import pprint

config = {
  'host': '54.241.98.140:27017',
  'username': 'app_user',
  'password': 'rechazo',
  'authSource': 'cc_db'
}
client = MongoClient(**config)
db = client.cc_db

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
    new_sig = db.norms.bulk_write(
        [UpdateOne({'_id': doc['_id'],'signatures': {'$exists': False}},{'$set': {'signatures':doc['signatures']}}) for doc in update]
    )
    for doc in update:
        if not db.norms.find_one({'_id':doc['_id']}):
            db.norms.insert_one(doc)
    print('Updating signatures in Norm Proposals from "norms"')
    pprint(new_sig.bulk_api_result)
    if new_sig.modified_count == 0:
        print('Updated: No new documents')

update_signatures()


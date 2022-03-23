from pymongo import MongoClient, UpdateOne
import urllib.request
import xmltodict
from pprint import pprint

config = {
  'host': '54.241.98.140:27017',
  'username': 'app_user',
  'password': 'rechazo',
  'authSource': 'cc_db'
}
client = MongoClient(**config)
db = client.cc_db


def get_members():
    """Gets Assemblymembers' data as a dictionary"""
    api_url = 'https://www.cconstituyente.cl/WSConvencionConstitucional/WSConvencionConstitucional.asmx/getListaConvencionales'
    contents = urllib.request.urlopen(api_url).read()
    members = xmltodict.parse(contents)['Convencionales']['Convencional']
    members = [{field[0]:field[1] for field in member.items()} for member in members]
    return members

def upsert_members():
    print('Updating "members" collection:')
    members = get_members()
    res = db.norms.bulk_write(
        [UpdateOne({'ConvencionalId':doc['ConvencionalId']}, {'$set': doc}, upsert=True) for doc in members]
        )
    pprint(res.bulk_api_result)
    if res.modified_count == 0:
        print('Updated: No new documents')


upsert_members()
#db.drop_collection('members')
#members = get_members()
#with open('Data/members.json', 'w') as fp:
#    json.dump(members, fp)

#!mongoimport --db cc_db --collection members --jsonArray --file Data/members.json 


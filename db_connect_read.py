from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


def setup_client():
	"""Returns connection to db"""
	print('Connecting to database...')
	config = {
	  'host': '54.241.98.140:27017',
	  'username': 'app_read',
	  'password': 'app_read',
	  'authSource': 'cc_db'
	}
	client = MongoClient(**config)

	try:
	   # The ismaster command is cheap and does not require auth.
	    client.admin.command('ismaster')
	    print('Connection to database successful')
	    return client
	except ConnectionFailure as e:
	    print("Server not available")
	    logging.error(f'Could not connect to db: {e}')
	except OperationFailure as failure:
	    print(failure)
	    logging.error(f'{failure}')


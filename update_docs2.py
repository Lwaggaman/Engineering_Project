import os
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time, random
import numpy as np
import geckodriver_autoinstaller
from selenium.common.exceptions import ElementClickInterceptedException
from pymongo import InsertOne, UpdateOne
import re
from pymongo import MongoClient
from text_funcs import clean_id
from time import sleep
from collections import defaultdict
from pprint import pprint
import logging
import contextlib
import sys
from tqdm import tqdm

logging.basicConfig(filename='docs.log',datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

#DummyFile is a slight modification from code by Perceval W
#https://stackoverflow.com/questions/36986929/redirect-print-command-in-python-script-through-tqdm-write
class DummyFile(object):
    def __init__(self, file):
        self.file = file

    def write(self, x):
        tqdm.write(x, end="", file=self.file)

    def __eq__(self, other):
        return other is self.file

    def flush(self):
        pass

#nostdout is by Pierre Schroeder at https://stackoverflow.com/questions/36986929/redirect-print-command-in-python-script-through-tqdm-write
@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile(save_stdout)
    yield
    sys.stdout = save_stdout

#Connect to DB
from db_connection import setup_client

client = setup_client()
db = client.cc_db

#Initialize driver for scraping
geckodriver_autoinstaller.install()
driver = webdriver.Firefox()
#driver.implicitly_wait(60)

def scrape_page():
    global page_nr
    #Get HTML elements
    soup = bs(driver.page_source, features="lxml")
    table_odd = soup.find(id='tableIniciativas').find_all(class_='odd')
    table_even = soup.find(id='tableIniciativas').find_all(class_='even')
    
    # Separate elements into docs
    page_docs = []
    for i in range(5):
        page_docs.append(table_even[i].find_all('td'))
        page_docs.append(table_even[i].find_all('td'))
    
    # Format for db
    page_dicts = []
    for doc in page_docs:
        doc_dict = {'_id': clean_id(doc[2].text)}
        doc_dict['name'] = doc[1].text
        doc_dict['topic'] =  doc[3].text
        doc_dict['commision'] = doc[4].text
        try:
            doc_dict['url'] = doc[5].find('a')['href']
        except TypeError:
            logging.info(f"Doc {doc_dict['_id']} contains no URL")
        page_dicts.append(doc_dict)
    logging.info(f'{len(page_dicts)} url in page {page_nr}')
    return page_dicts

def next_page():
    global driver, page_nr
    next_button = driver.find_element(by='id', value='tableIniciativas_next')
    try:
        next_button.click()
    except ElementClickInterceptedException as e:
        driver.execute_script("arguments[0].click();", next_button)
        logging.info(f'Element not clickable in page {page_nr}: "Next" button alternate location found')
    sleep(1.2)
    page_nr += 1

def update_db_docs():
    #geckodriver_autoinstaller.install()
    global driver, page_nr
    #driver = webdriver.Firefox()
    driver.implicitly_wait(60)
    driver.get('https://www.chileconvencion.cl/iniciativas-normas/')
    
    update_docs = True
    page_nr = 1
    new_docs = scrape_page()

    #Loop crawls through pages until it reaches one where all the data is already in the db.
    nr_res = defaultdict(int) #Tracks all bulk api results (done sequentially to avoid bloating memory)
    while update_docs == True:
        for doc in new_docs: 
            if db.norms.find_one({'_id':doc['_id']}):
                new_docs.remove(doc)
        print(f'{len(new_docs)} new proposals found in page {page_nr}')
        logging.info(f'{len(new_docs)} new urls in page {page_nr}')
        
        if len(new_docs)==0: #No new documents, loop stops
            logging.info(f'No new docs in page {page_nr}: Scraping will stop')
            update_docs = False 

        else: #upsert docs found, scrape next page
            try: 
                res = db.norms.bulk_write(
                    [UpdateOne({'_id':doc['_id']}, {'$set': doc}, upsert=True) for doc in new_docs]
                    )
                [logging.info(f'Upserted URL of document {ups["_id"]}') for ups in res.bulk_api_result["upserted"]]            
            
            except BulkWriteError as bwe:
                [logging.info(f"{ups['_id']} has updated text") for ups in bwe.details['upserted']]
                [logging.error(f"failed to insert {error['op']['_id']} : {error['errmsg']}") for error in bwe.details['writeErrors']]
                #print(f"Updated:{bwe.details['nUpserted']} new documents with text")

            next_page()
            new_docs = scrape_page()
            #for key, value in res.bulk_api_result.items():
            #    if type(value) == int:
            #        nr_res[key] += value

    print(f'Scraped {page_nr - 1} pages')
    #pprint(nr_res)
    #print(f'Matched: {nr_res['nMatched']}, Inserted: {nr_res['nInserted']}, Modified: {nr_res['nModified']}')


update_db_docs()
import logging
from pdf2image import convert_from_path
import pytesseract
import textract
import platform
from fake_useragent import UserAgent
from pymongo import MongoClient
from text_funcs import remove_singles
from db_connection import setup_client
from tqdm import tqdm

client = setup_client()
db = client.cc_db

def get_pdf(url):
    ua = UserAgent()
    try:
        response = requests.get(url, headers={'User-Agent':str(ua.random)})
    except BaseException as error:
        logging.warning(f'{error} at {url},attempting another useragent')
        try:
            time.sleep(np.random.uniform(0,4))
            response = requests.get(url, headers={'User-Agent':str(ua.random)})
        except BaseException as error:
            logging.error(f'Failed to extract from :{url}, attempted waiting and different useragent')
            print(f'Failed to extract from :{url}')
            raise Exception(f'{error}')
    logging.info(f'Text extracted from {_id} successfully')
    with open(f'Data/temporary.pdf', 'wb') as f:
            f.write(response.content)
            
def get_text(id_):
    try:
        text = textract.process('Data/temporary.pdf', method='pdfminer')
    except UnicodeDecodeError: #BaseException as error:
        logging.warning(f'Convension error extracting text from {id_}, attempting OCR')
        return get_text_ocr()
    if len(text) < 50:
        logging.warning(f'Failed to use textract in {id_}, attempting OCR')
        return get_text_ocr()
    return conv_chars(text)

def get_text_ocr():
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    else:
        pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'        
    pages = convert_from_path(f'Data/temporary.pdf', 350)
    text = []
    for page in pages: #GENERATOR WOULD BE BETTER, CHANGE IF TIME
        page = str(pytesseract.image_to_string(page, lang='spa'))
        text.append(page)
    text = ' '.join(str(text_) for text_ in text)
    return remove_singles(conv_chars(text))

def update_text():
    nr_wo_text = db.norms.count_documents({'url':{'$exists':True}, 'text':{'$exists':False}})
    print(f'{nr_wo_text} URLs without text found.')
    db_docs = db.norms.find({'text':{'$exists':False}}, {'url':1})
    print('Extracting text...')
    for doc in tqdm(db_docs, total=nr_wo_length):
        _id = doc['_id']
        get_pdf(doc['url'])
        text = get_text(_id)
        db.norms.update_one({'_id':doc['_id']}, {'$set': {'text':text}})
        logging.info(f'{_id} has updated text')

update_text()

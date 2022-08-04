import logging
from pdf2image import convert_from_path
import requests
import pytesseract
import textract
import platform
from fake_useragent import UserAgent
from pymongo import MongoClient
from text_funcs import remove_singles, conv_chars, decode_text
from db_connection import setup_client
from tqdm import tqdm
import contextlib
import sys

client = setup_client()
db = client.cc_db

#logging.basicConfig(filename='text.log', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='text.log',datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

class DummyFile(object):
    def __init__(self, file):
        self.file = file

    def write(self, x):
        tqdm.write(x, end="", file=self.file)

    def __eq__(self, other):
        return other is self.file

    def flush(self):
        pass

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile(save_stdout)
    yield
    sys.stdout = save_stdout

class PdfError(Exception):
    """Problem downloading PDF, unencountered before. Flag to continue to next url."""
    pass
continue_pdf = PdfError()

def get_pdf(url):
    """
    Copy of PDF document is downloaded from URL and saved to local memory.
    """
    ua = UserAgent()
    try:
        response = requests.get(url, headers={'User-Agent':str(ua.random)})
    except BaseException as error:
        logging.warning(f'{error} at {url},attempting another useragent')
        pbar.set_description(f'Error encountered. Attempting with another User Agent')
        try:
            time.sleep(np.random.uniform(0,4))
            response = requests.get(url, headers={'User-Agent':str(ua.random)})
        except BaseException as error:
            logging.error(f'{error}: Failed to download from :{url}, attempted waiting and different useragent')
            print(f'Failed to extract from :{url}')
            raise continue_pdf
    #logging.info(f'PDF downloaded from {url} successfully')
    with open(f'Data/temporary.pdf', 'wb') as f:
            f.write(response.content)
            
def get_text(id_):
    global pbar
    """
    Attempts to extract text from PDF.
    If a scanned document is encountered, it runs function that performs OCR.
    """
    try:
        text = textract.process('Data/temporary.pdf', method='pdfminer')
    except UnicodeDecodeError: #BaseException as error:
        logging.warning(f'Conversion error extracting text from {id_}, attempting OCR')
        return get_text_ocr()
    if len(text) < 50:
        pbar.set_description('Reattempting text extraction with OCR')
        logging.warning(f'Failed to use textract in {id_}, attempting OCR')
        return get_text_ocr(id_=id_)
    else:
        logging.info(f'text extracted from PDF for {id_}')
    return decode_text(text)

def get_text_ocr(id_):
    """
    Attempts to extract text from PDF by converting to image and performing Optical Character Recognition.
    """
    global pbar
    poppler_path = "/usr/local/Cellar/poppler/22.06.0_1/bin"
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    else:
        pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'        
    
    
    pbar.set_description('Converting PDF to images')
    pages = convert_from_path(f'Data/temporary.pdf', 350, poppler_path=poppler_path)
    
    pbar.set_description('Extracting text from images')
    text = []
    for page in pages: #GENERATOR WOULD BE BETTER, CHANGE IF TIME
        page = str(pytesseract.image_to_string(page, lang='spa'))
        text.append(page)
    text = ' '.join(str(text_) for text_ in text)
    logging.info(f'text extracted with OCR for {id_}')
    return remove_singles(conv_chars(text))

def update_text():
    """
    Searches for urls in db's norms collection that do not have text.
    It iterates through them, saving a copy of pdf from url to local memory before extrating
    text and saving it to the corresponding text field in collection. Only one copy at a time in memory.
    If PDF consists of a scanned document, optical character recognition if performed.
    Updates and errors are logged.
    """
    nr_wo_text = db.norms.count_documents({'url':{'$exists':True}, 'text':{'$exists':False}})
    print(f'{nr_wo_text} URLs without text found.')

    db_docs = db.norms.find({'text':{'$exists':False}}, {'url':1})
    print('Extracting text...')

    with nostdout():
        global pbar
        pbar = tqdm(total=nr_wo_text)
        for doc in db_docs:
            _id = doc['_id']

            pbar.set_description('Downloading PDF from URL')
            try:
                get_pdf(doc['url'])
            except PdfError:
                continue

            pbar.set_description('Extracting text from PDF')
            text = get_text(_id)

            pbar.set_description('Upserting text to database')
            db.norms.update_one({'_id':doc['_id']}, {'$set': {'text':text}})
            
            logging.info(f'{_id} has updated text')
            pbar.update(n=1)

update_text()

from pdf2image import convert_from_path
import pytesseract
import textract
import platform
from fake_useragent import UserAgent

config = {
  'host': '54.241.98.140:27017',
  'username': 'app_user',
  'password': 'rechazo',
  'authSource': 'cc_db'
}
client = MongoClient(**config)
db = client.cc_db

def get_pdf(url):
    ua = UserAgent()
    try:
        response = requests.get(url, headers={'User-Agent':str(ua.random)})
    except BaseException as error:
        try:
            time.sleep(np.random.uniform(0,4))
            response = requests.get(url, headers={'User-Agent':str(ua.random)})
        except BaseException as error:
            print(f'Failed to extract from :{url}')
            raise Exception(f'{error}')
    with open(f'Data/temporary.pdf', 'wb') as f:
            f.write(response.content)
            
def get_text():
    try:
        text = textract.process('Data/temporary.pdf', method='pdfminer')
    except UnicodeDecodeError: #BaseException as error:
        raise Exception(f'UnicodeDecodeError') 
    if len(text) < 50:
        return get_text_ocr()
    return text

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
    return text

def update_text():
    elements = db.norms.find({'text':{'$exists':False}}, {'url':1})
    for elem in elements:
        get_pdf(elem['url'])
        text = get_text()
        text = conv_chars(text)
        db.norms.update_one({'_id':elem['_id']}, {'$set': {'text':text}})

update_text()

import re

def clean_id(string):
    string = re.sub(r'opu', r'\#', re.sub(r'nd', r'\%', string))
    return re.sub(r'[^\d\-\%\#]', r'', string)

utf_chars = ({r'\\xc3\\xa1':r'á',r'\\xc3\\xa9':r'é',r'\\xc3\\xad':r'í',r'\\xc3\\xb3':r'ó',
             r'\\xc3\\xba':r'ú',r'\\xc3\\xb1':r'ñ',r'\\xef\\xac\\x81':r'fi',
             r'\\xe2\\x80\\x9c':r'"',r'\\xe2\\x80\\x9d':r'"',r'\\xef\\xac\\x82':r'fl',
             r'\\xc2\\xb0':r'',r'\\xc3\\x93':r'Ó',r'\\xc2\\xba':r'',r'\\xc3\\x91':r'Ñ',
             r'\\xe2\\x80\\x93':r'-',r'\\xc3\\x81':r'Á',r'\\xc3\\x8d':r'Í',r'\\xc2\\xa1':r'',
             r'\\xef\\x82\\xb7':r'','\xc2\xab':r'','\xc2\xbb':r'',r'\\x0c':r'',r'(?<=\w)([\\]n)((?=[a-z]))':r' '})

replacements = {'\x0c': '', '\n \n':'--NEWLINE--', '\n':' ', '--NEWLINE--':r'\n'}

def conv_chars(string, chars=utf_chars):
    """ Converts spanish characters from UTF """
    #string = string.decode('utf-8')
    for orig, repl in chars.items():
        string = re.sub(orig, repl, string)
    return string

def decode_text(text, chars=replacements):
    text = text.decode('utf-8')
    for orig, repl in chars.items():
        text = re.sub(orig, repl, text)
    return text
def remove_singles(string):
    string = re.sub(r'[^\w\s\.\,]', r'', string) #remove spec chars
    string = re.sub(r'\sy\s', r' $& ', string) #Hide 1-digit chars
    string = re.sub(r'\so\s', r' or ', string)
    string = re.sub(r'\se\s', r' edei ', string)
    string = re.sub(r'\sa\s', r' adea ', string)
    string = re.sub(r'\su\s', r' udeo ', string)
    string = re.sub(r'\s.\s', r'', string) #remove 1-digit words
    string = re.sub(r'\s\$&\s', r' y ', string) #recover 1-digit chars
    string = re.sub(r'\sor\s', r' o ', string)
    string = re.sub(r'\sedei\s', r' e ', string)
    string = re.sub(r'\sadea\s', r' a ', string)
    string = re.sub(r'\sudeo\s', r' u ', string)
    return string

#print(clean_id('Boletín 1007-6'))


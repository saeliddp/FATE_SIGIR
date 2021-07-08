'''
Created on Sep 27, 2018
for process_text method,
refer to:
https://nlpforhackers.io/recipe-text-clustering/

@author: rg522
@author: saeliddp
'''
import requests
import traceback
# from bs4 import BeautifulSoup
import re
# from gensim import corpora
import html2text
import os
# from config import stopwordList, wordDictFile
import string
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from config import stopword_list
from nltk.corpus import stopwords

def plainText(url):
    '''
    convert html to plain text
    :param str:
    '''  
    try:
        page = requests.get(url).text
        page = keepUnicodeChar(page)
    #     soup = BeautifulSoup(page, 'html.parser')
    #     return soup.get_text()
    #     return html_to_text(page)
    
        h = html2text.HTML2Text()
        # Ignore converting links from HTML
        h.ignore_links = True
        h.images_to_alt = True
        h.escape_snob = True
        h.ignore_emphasis = True
    
        text = h.handle(page)
        text = unify(text)
        text_tokens = process_text(text)
        text = ' '.join(text_tokens)
        return text
    except Exception as e:
        print(e)
        traceback.print_exc()
        return ''
    return ''

def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english')) 
    
    tokens_cpy = []
    for t in tokens:
        if t not in stop_words:
            tokens_cpy.append(t)
    tokens = tokens_cpy
    
    if stem:
        tokens_cpy = []
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]
        for t in tokens:
            if t not in stopword_list:
                tokens_cpy.append(t)
        tokens = tokens_cpy
    return tokens

def unify(s):
    '''
    normalize extra spaces, numbers, and links
    remove punctuation
    '''
    s = re.sub('\s+', ' ', s)
    s = s.lower()
    s = re.sub('https?://[^\s()]+', 'thisislink,', s)
    s = re.sub('[a-z0._]+@[a-z0.-]+[a-z]','thisisemail',s)
#     s = re.sub('[^a-z0-9_\s]', '', s) # remove punctuation
    s = re.sub('['+string.punctuation+']', '', s)  # remove punctuation
    s = re.sub('[-]+','-', s)
    s = re.sub('\d+', '0', s)
    s = re.sub('\d+', '0', s)
    s = re.sub('\s[a-z0-9]{19,}\s',' ',s)
    s = re.sub('\s[a-z_]{1}\s',' ',s)
    s = re.sub('\s+', ' ',s)
    s = re.sub('\s+', ' ',s)
    return s

def keepUnicodeChar(s, rangeArray=[]):
    if not rangeArray:
        # ascii map
        rangeArray = range(128)
    s_cpy = ''
    for c in s:
        if c and ord(c) in rangeArray:
            s_cpy += c
    return s_cpy.strip()

def getDoc(docDir):
    for fname in os.listdir(docDir):
        if '.txt' not in fname:
            continue
        doc = open(docDir+fname, encoding='utf-8').read().strip()
        if doc:
            tokens = process_text(doc)
            doc = ' '.join(tokens)
            yield int(fname.replace('.txt', '')), doc   #rank,text

def getDocList(docDir):
    return [doc for _,doc in getDoc(docDir)]

def main():
    pass

if __name__ == '__main__':
    main()
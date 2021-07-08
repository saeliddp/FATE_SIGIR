'''
Created on Oct 6, 2018
reference:
@author: rg522
'''

import collections
# from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
# from pprint import pprint
import pickle
import string
# from nltk.tokenize import word_tokenize
# from nltk.stem.porter import PorterStemmer
from config import queryDocDir_list
import os
import re
import sys
#from sklearn.metrics.cluster.unsupervised import silhouette_score
 
def cluster_texts(texts, clusters=2):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(
#         tokenizer=process_text,
#                                  stop_words=stopwords.words('english'),
#                                  stop_words = stopword_list,
                                 max_df=0.5, #0.pip5
                                 min_df=0.2, #0.2
                                 lowercase=True)
    tfidf_model = vectorizer.fit_transform(texts)
    try:
        km_model = KMeans(n_clusters=clusters, 
                          random_state=3, 
                          )
        km_model.fit(tfidf_model)
        clustering = collections.defaultdict(list)
        
#         sil_ave = silhouette_score(tfidf_model, km_model.labels_,
#     #                                metric='euclidean',
#     #                                 metric='cosine',
#                                     )
    except:
#         return None,None
        return None
    
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
#     return clustering, sil_ave
    return clustering
 

def unify(s):
    '''
    normalize extra spaces, numbers, and links
    remove punctuation
    '''
    s = re.sub('[ \t]+', ' ', s)
    s = re.sub('\n+', '\n', s)
    s = s.lower()
    s = re.sub('\d+', '0', s)
    s = re.sub('https?://[^\s()]+', 'THISISALINK,', s)
    s = re.sub('[a-z0._]+@[a-z0.-]+[a-z]','THISISANEMAIL',s)
    s = re.sub('[^a-zA-Z0-9_\s]', '', s) # remove punctuation
    s = re.sub('\s+', ' ',s)
    return s

def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    table = str.maketrans(dict.fromkeys(string.punctuation))
    text = text.translate(table)
    tokens = word_tokenize(text.lower())
    return tokens

def getDoc(docDir, docID_rank_dict):
    # for nyt dataset
    for fname in os.listdir(docDir):
        if '.txt' not in fname:
            continue
        docID = fname.replace('.txt', '')
        if docID not in docID_rank_dict:
            continue
        rank = docID_rank_dict[docID]
        if int(rank) > 100:
            continue
        doc = open(os.path.join(docDir, fname)).read().strip()
        if doc:
#             doc = unify(doc)
#             tokens = process_text(doc)
#             if not tokens: 
#                 continue
#             doc = ' '.join(tokens)
            yield rank, doc   #docID,text


def prep_docs(docDir):
    '''
    @return: doc_list for clustering
    generate dict of index:rank of doc to locate snippet
    '''
    i_s_dict = dict()   # idx:rank
    doc_list = []
    with open(docDir + 'docID_rank.dict', 'rb') as fi:
        docID_rank_dict = pickle.load(fi)
    for rank, doc in getDoc(docDir, docID_rank_dict):
        doc_list.append(doc)
        i_s_dict[len(doc_list)-1] = rank
    with open(docDir + 'idx_rank.pickle', 'wb') as fw:
        pickle.dump(i_s_dict, fw,2)
    with open(docDir + 'docs.pickle','wb') as fw:
        pickle.dump(doc_list, fw)
    return doc_list


def main():
#===============================================================================
# google dataset
#===============================================================================
#-------
# step 1. prepare doc list
# use python3 cluster_prep.py
#------
# step 2. generate cluster:id file
#------ 
    for docDir in queryDocDir_list:
        doc_list = []
        with open(docDir + 'docs.pickle', 'rb') as fr:
            doc_list = pickle.load(fr)
        clusters = cluster_texts(doc_list, 2)
        with open(docDir + 'cluster.dict', 'w') as fw:
            for c,doc_idx in dict(clusters).items():
                fw.write(str(c))
                fw.write(':')
                fw.write(','.join([str(i) for i in doc_idx]))
                fw.write('\n')          
#------
# step 3. generate cluster:rank file
#------    
    for docDir in queryDocDir_list:
        i_s_dict = dict()
        with open(docDir + 'idx_rank.pickle', 'rb') as fr:
            i_s_dict = pickle.load(fr)
               
        data = open(docDir + 'cluster.dict','r').readlines()
        with open(docDir + 'cluster_rank.dict', 'w') as fw:
            for line in data:
                c, idx_list = line.split(':')
                idx_list = idx_list.strip().split(',')
                idx_list = [int(i) for i in idx_list]
                rank_list = sorted([ i_s_dict[i] 
                                    for i in idx_list])
                fw.write(c)
                fw.write(':')
                fw.write(','.join([str(i) for i in rank_list]))
                fw.write('\n')
         

                    
if __name__ == "__main__":
    main()
    
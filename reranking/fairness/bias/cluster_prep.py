'''
Created on Oct 6, 2018
reference:
@author: rg522
'''


from preprocess import getDoc
import pickle
from config import queryDocDir_list

 

def prep_docs(docDir):
    '''
    @return: doc_list for clustering
    generate dict of index:rank of doc to locate snippet
    '''
    i_s_dict = dict()
    doc_list = []
    for rank,doc in getDoc(docDir):
        doc_list.append(doc)
        i_s_dict[len(doc_list)-1] = rank
    with open(docDir + 'idx_rank.pickle', 'wb') as fw:
        pickle.dump(i_s_dict, fw)
    with open(docDir + 'docs.pickle','wb') as fw:
        pickle.dump(doc_list, fw)
    return doc_list

def main():
    for docDir in queryDocDir_list:
        doc_list = prep_docs(docDir)   # put docs here
#     clusters = cluster_texts(doc_list, 2)
#     pprint(dict(clusters))
 
if __name__ == "__main__":
    main()
    
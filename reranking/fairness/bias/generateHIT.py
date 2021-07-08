# -*- coding: utf-8 -*-
'''
Created on Oct 1, 2018

@author: rg522
@author: saeliddp
'''
import re
from classes.snippet import Snippet, QuerySnippet
import pickle
from config import snippetFile_original, snippetPickle, queryDocDir_list
import random
from preprocess import keepUnicodeChar, plainText
import os
import csv

def readResultFile(frname, fwname, docDir_list):
    '''
    file format example:
    Query 1 = [﻿aretha franklin funeral]
    Rank=1
    TITLE=Aretha Frank...
    URL=https://www.newyorker.com
    DESC=funeral
    Rank=2
    ...
    
    @return: query_snippet_list
    '''
    count_q = 0
    query_snippet_list = []
    with open(frname, 'r', encoding='utf-8') as fr:
        for line in fr:
            #line = keepUnicodeChar(line)
            #line = line.encode('ascii', 'ignore')
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('Query'):
                count_q += 1
               
                q = re.sub('^Query \d+ = ', '', line)
                print(count_q,':',q)
                if (query_snippet_list and 
                    not query_snippet_list[-1].snippetList):
                    # previous query has empty results
                    query_snippet_list[-1] = QuerySnippet(q)
                else:
                    query_snippet_list.append(QuerySnippet(q))
            elif line.startswith('Rank'):
                r = re.sub('^Rank=', '', line)
                query_snippet_list[-1].add_snippet(Snippet())
                query_snippet_list[-1].snippetList[-1].set_rank(r)
            elif line.startswith('TITLE'):
                t = re.sub('TITLE=', '', line)
                query_snippet_list[-1].snippetList[-1].set_title(t)
            elif line.startswith('DESC'):
                query_id = count_q
                docDir = docDir_list[query_id-1]
                fname = docDir + r + '.txt'
                #if not os.path.isfile(fname):
                    #query_snippet_list[-1].snippetList.pop()
                #else:
                d = re.sub('^DESC=', '', line)
                query_snippet_list[-1].snippetList[-1].set_desc(d)
            elif line.startswith('URL'):
                u = re.sub('^URL=', '', line)
                r = query_snippet_list[-1].snippetList[-1].get_rank()
                query_snippet_list[-1].snippetList[-1].set_url(u)
                query_id = count_q  # starts from 1
                docDir = docDir_list[query_id-1]
                fname = docDir + r + '.txt'
                if not os.path.isfile(fname):
                    print('scraping for:', u)
                    doc = plainText(u)  # get text from url
                    if doc:
                        with open(fname,'w', encoding='utf-8') as fw:                  
                            fw.write(doc)
            else:
                # append remaining desc
                query_id = count_q
                docDir = docDir_list[query_id-1]
                fname = docDir + r + '.txt'
                #if os.path.isfile(fname):
                d = query_snippet_list[-1].snippetList[-1].get_desc()
                query_snippet_list[-1].snippetList[-1].set_desc(d + line)
 

 
    with open(fwname, 'wb') as fw:
        pickle.dump(query_snippet_list, fw)
        

def combine_snippet_file(f1, f2, fwname):
    with open(f1, 'rb') as fr:
        list1 = pickle.load(fr)
    with open(f2, 'rb') as fr:
        list2 = pickle.load(fr)
    lw = list1 + list2 
    with open(fwname, 'wb') as fw:
        pickle.dump(lw, fw)

def main():
    readResultFile(snippetFile_original, snippetPickle, queryDocDir_list)

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
'''
Created on Oct 1, 2018

@author: rg522
@author: saeliddp
'''
import re
from classes.snippet import Snippet, QuerySnippet
import pickle
import random
import os

def main():
    count_q = 0
    query_snippet_list = []
    with open('scraping_results.txt', 'r', encoding='utf-8') as fr:
        for line in fr:
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
                t = re.sub('^TITLE=', '', line)
                query_snippet_list[-1].snippetList[-1].set_title(t)
            elif line.startswith('DESC'):
                d = re.sub('^DESC=', '', line)
                query_snippet_list[-1].snippetList[-1].set_desc(d)
            elif line.startswith('URL'):
                u = re.sub('^URL=', '', line)
                query_snippet_list[-1].snippetList[-1].set_url(u)
                
            else:
                # append remaining desc
                d = query_snippet_list[-1].snippetList[-1].get_desc()
                query_snippet_list[-1].snippetList[-1].set_desc(d + line)
        
    with open('fake_results.txt', 'r', encoding='utf-8') as fr:
        fake_lines = fr.readlines()
    
    google_lines = []
    altered_lines = []
    for i, qs in enumerate(query_snippet_list):
        gl = ["%dX Q0 %d00%s %d g\n" % (i + 1, i + 1, snip.get_rank(), j + 1) for j, snip in enumerate(qs.snippetList[:10])]
        al = gl.copy()
        new_rank = int(qs.snippetList[-1].get_rank()) + 1
        # get rid of query line
        fake_lines.pop(0)
        # get rid of fake 1 line
        fake_lines.pop(0)
        t1 = re.sub('^TITLE=', '', fake_lines.pop(0))
        u1 = re.sub('^URL=', '', fake_lines.pop(0))
        d1 = re.sub('^DESC=', '', fake_lines.pop(0))
        qs.add_snippet(Snippet())
        qs.snippetList[-1].set_rank(new_rank)
        qs.snippetList[-1].set_title(t1)
        qs.snippetList[-1].set_desc(d1)
        qs.snippetList[-1].set_url(u1)
        randindex = random.randint(0, 4)
        al[randindex] = "%dX Q0 %d00%d %d g\n" % (i + 1, i + 1, new_rank, randindex + 1)
        
        if len(fake_lines) > 0 and fake_lines[0].startswith('Fake'):
            # get rid of fake 2 line
            new_rank += 1
            fake_lines.pop(0)
            t2 = re.sub('^TITLE=', '', fake_lines.pop(0))
            u2 = re.sub('^URL=', '', fake_lines.pop(0))
            d2 = re.sub('^DESC=', '', fake_lines.pop(0))
            qs.add_snippet(Snippet())
            qs.snippetList[-1].set_rank(new_rank)
            qs.snippetList[-1].set_title(t1)
            qs.snippetList[-1].set_desc(d1)
            qs.snippetList[-1].set_url(u1)
            randindex = random.randint(5, 9)
            al[randindex] = "%dX Q0 %d00%d %d g\n" % (i + 1, i + 1, new_rank, randindex + 1)
        google_lines.extend(gl)
        altered_lines.extend(al)


    with open('generated_data/snippet.pickle', 'wb') as fw:
        pickle.dump(query_snippet_list, fw)
    
    with open('generated_data/google.txt', 'w') as fw:
        google_lines[-1] = google_lines[-1][:-1]
        fw.writelines(google_lines)
    
    with open('generated_data/altered.txt', 'w') as fw:
        altered_lines[-1] = altered_lines[-1][:-1]
        fw.writelines(altered_lines)

if __name__ == '__main__':
    main()
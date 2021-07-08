'''
Created on Sep 19, 2018

@author: rg522
'''
from config import *
import pickle
import random

alg_str_dict = {
        'top-top':'t',
        'page-wise':'p',
        'top-top_p':'tp',
        'page-wise_p':'pp',  
        'random':'r',
        'random_p':'rp',
        'greedy':'g',
        'greedy_fair':'gf',
        'greedy_fair_p':'gfp',
        }

def n_pick(n1, n2, p):
    '''
    compute number of documents to pick from each cluster
    @param n_c1,n_c2: lenght of each cluster
    @param p: proportion of total c1
    ''' 
    n_c1 = int(round(p*10))
    n_c2 = 10 - n_c1
    if n1 < n_c1:   # not enough items in c1
        n_c1 = n1
        n_c2 = 10 - n1
    elif n2 < n_c2: # not enough items in c2
        n_c2 = n2
        n_c1 = 10 - n_c1
    return n_c1, n_c2

def sort_rank(r_list):
    '''
    sort string list based on integer order
    @param r_list: list of string
    @return: list of string ranked based on integer value
    '''
    try:
        r_list = [int(r) for r in r_list]
        r_list = sorted(r_list)
        r_list = [str(r) for r in r_list]
    except Exception as e:
        print(e)
        print(r_list)
        raise
    return r_list

def pick_top(c1, c2, p=0.5):
    '''
    pick top 5 from each cluster
    @param p:  proportion of c1
    if c1 is non-zero, pick top p*10 from c1, 
    10(1-p) from c2 
    '''
    n_c1,n_c2 = n_pick(len(c1), len(c2), p)
    c1_rank_list = [ c1[i] for i in range(n_c1)]
    c2_rank_list = [ c2[i] for i in range(n_c2)]
#     print 'top-top_p=:',p
    return sort_rank(c1_rank_list + c2_rank_list)

def pick_random(c1, c2, p=0.5):
    '''
    randomly pick 5 from each cluster
    '''
    n_c1,n_c2 = n_pick(len(c1), len(c2), p)
    c1_cpy = c1
    c2_cpy = c2
    random.shuffle(c1_cpy)
    random.shuffle(c2_cpy)
    c1_rank_list = [ c1_cpy[i] for i in range(n_c1)]
    c2_rank_list = [ c2_cpy[i] for i in range(n_c2)]
    return sort_rank(c1_rank_list + c2_rank_list)
   
def page_wise(c1, c2, p=0.5):
    '''
    pick top 1 from each cluster on each page
    @return: r_list
    @rtype: list of [cluster_index, rank_index] 
    '''
    c1_rank_list = []
    c2_rank_list = []
    n_c1,n_c2 = n_pick(len(c1), len(c2), p)
    
    count_c1 = 0
    count_c2 = 0
    buff = []   # stores unused results
    for r in c1:
        lo = 10*count_c1
        hi = 10*count_c1+9
        if int(r) < lo:
            buff.append(r)
        elif int(r) > hi:
            # this page does not contain requested item
            # check buff
            if not buff:
                # buff empty, use next page item
                c1_rank_list.append(r)
            else:
                c1_rank_list.append(buff.pop(-1))
            count_c1 += 1
        else:
            c1_rank_list.append(r)
            count_c1 += 1   
        if count_c1 >= n_c1:
            break
    
    buff = []
    for r in c2:
        lo = 10*count_c2
        hi = 10*count_c2+9
        if int(r) < lo:
            buff.append(r)
        elif int(r) > hi:
            if not buff:
                c2_rank_list.append(r)
            else:
                c2_rank_list.append(buff.pop(-1))
            count_c2 += 1
        else:
            c2_rank_list.append(r)
            count_c2 += 1   
        if count_c2 >= n_c2:
            break
#     print 'c2:',c2
#     print 'top10:',c2_rank_list
    return sort_rank(c1_rank_list + c2_rank_list)


def eps_greedy_top(c1, c2, eps):
    '''
    no proportion needed.
    with probability 1-eps, select the top document
    with probability eps, select from the rest of the list

    * does not guarantee fairness
    '''
    all_list = sort_rank(c1 + c2)
    top_10 = all_list[:10]
    rest_list = all_list[10:]
    total_list = top_10 + rest_list
    r_list = []
    for _ in range(10):
        if random.random() >= eps:
            # p = 1-eps
            # select top
            r_list.append(top_10.pop(0))
            total_list.pop(0)
        else:
            # explore rest or total?
            # currently select from total
#             i = random.randint(0,len(rest_list)-1)
#             r_list.append(rest_list.pop(i))
            i = random.randint(0,len(total_list)-1)
            item = total_list.pop(i)
            r_list.append(item)
            if item in top_10:
                top_10.remove(item)
    return sort_rank(r_list)


def eps_greedy_fair(c1, c2, eps, p=0.5):
    '''
    with probability 1-eps, select from cluster 
    that best satisfies fairness;
    with probability eps, select randomly from any cluster
    when picking from within cluster, always pick top
    '''
    r_list = []
    count_c1 = 0
    count_c2 = 0
    
    # pick the top as the first one
    if c1[0] < c2[0]:
        r_list.append(c1[0])
        count_c1 += 1
    else:
        r_list.append(c2[0])
        count_c2 += 1
        
    # pick the rest 9 documents
    for _ in range(1,10):
        if count_c1 >= len(c1):  # c1 exhausted
            r_list.append(c2[count_c2])
            count_c2 += 1
            continue
        if count_c2 >= len(c2):  # c2 exhausted
            r_list.append(c1[count_c1])
            count_c1 += 1
            continue
                
        if random.random() >= eps:
            # select best fit cluster
            # only need to check c1's proportion
            if count_c1 < p*len(r_list): 
                # pick from c1
                r_list.append(c1[count_c1])
                count_c1 += 1
            else:
                # pick from c2
                r_list.append(c2[count_c2])
                count_c2 += 1
        else:
            # explore rest
            if random.randint(0,1) == 0:
                # pick from c1
                r_list.append(c1[count_c1])
                count_c1 += 1
            else:
                r_list.append(c2[count_c2])
                count_c2 += 1

    return sort_rank(r_list)




def get_rankList(docDir, fname, eps=0):
    '''
    @param docDir: a query folder containing docs, cluster files
    @param fname: rerank_algorithm.txt 
    @param eps: eps-greedy param
        defaults 0 for picking top 10, 
        results are the same as original ranking.
    @return: rerank_list
    '''
    lines = open(docDir + 'cluster_rank.dict', 'r').readlines()
    line1 = lines[0].strip()    # c1
    line2 = lines[1].strip()    # c2

    _, c1 = line1.split(':')
    if not c1:
        return None
    c1 = c1.strip().split(',')
    _, c2 = line2.split(':')
    if not c2:
        return None
    c2 = c2.strip().split(',')
    if len(c1) + len(c2) < 20:
        return None
    
    p = len(c1) *1.0 / (len(c2)+len(c1))    # proportion of c1
    rank_list = []
    if 'top-top.txt' in fname:
        rank_list = pick_top(c1, c2)
    elif 'page-wise.txt' in fname:
        rank_list = page_wise(c1, c2)
    elif 'random.txt' in fname:
        rank_list = pick_random(c1, c2)
    elif 'greedy_fair.txt' in fname:
        rank_list = eps_greedy_fair(c1, c2, eps)
    # non fairness
    elif 'greedy.txt' in fname:
        rank_list = eps_greedy_top(c1, c2, eps)
    # disparate impact -- proportion
    elif 'top-top_p.txt' in fname:
        rank_list = pick_top(c1, c2, p)
    elif 'random_p.txt' in fname:
        rank_list = pick_random(c1, c2, p)
    elif 'page-wise_p.txt' in fname:
        rank_list = page_wise(c1, c2, p)
    elif 'greedy_fair_p.txt' in fname:
        rank_list = eps_greedy_fair(c1, c2, eps, p)
    return rank_list


def get_cluster_id(docDir):
    lines = open(docDir + 'cluster_rank.dict', 'r').readlines()
    line1 = lines[0].strip()    # c1
    line2 = lines[1].strip()    # c2
    _, c1 = line1.split(':')
    c1 = c1.strip().split(',')
    _, c2 = line2.split(':')
    c2 = c2.strip().split(',')

    return c1,c2



def repeat_rerank_trec(num_exp, alg, eps, folderPath=None):
    alg_str = alg_str_dict[alg]
    if 'greedy' in alg:
        alg_str = str(eps).replace('.', '') + alg_str
        
    outDir = repeat_rerankDir
                
    for i in range(num_exp):
        if folderPath is None:
            exp_dir = outDir + str(i) + '/'
        else:
            exp_dir = folderPath
        if not os.path.exists(exp_dir):
            os.makedirs(exp_dir)
            
        fname = exp_dir + alg_str + '.txt'
        write_rank_to_file_trec(fname, alg, eps)


            
            
def write_rank_to_file_trec(fname, alg,eps = 0):
    '''
    default eps=0: always pick top 10    
    trec format:
    topic_id=qid+cluster_id Q0 doc_id=qid+rid rank score=101-r groupid=algorithm_name
    '''
    fw = open(fname,'w')
        
    count_q = 0
    for docDir in queryDocDir_list:
        count_q += 1
        rank_list = get_rankList(docDir, alg+'.txt', eps)
        if not rank_list:
            continue
        c1,c2 = get_cluster_id(docDir)
        
        count_rank = 0
        for r in rank_list:
            count_rank += 1
            if r in c1:
                cid = '0'
            elif r in c2:
                cid = '1'
            else:
                continue
            cid = str(count_q) + cid
            doc_id = str(count_q) + '00' + r
            score = 101 - int(r)
            gid = alg_str_dict[alg]
            res_str = '%s Q0 %s %s %s %s\n'% (cid,doc_id,count_rank,score,gid)
            fw.write(res_str)
    fw.close()        
               
        

def main():
    eps_list = [0, 0.3, 0.5]
    # eps=0 is the same as top-top for fair
    # eps=0 is the same as google original rank for non-fair
    
    algList = [
        'greedy_fair_p',
        'greedy_fair',
        'greedy',
        ]
    num_exp= 1
    for alg in algList:
        print(alg)
        for eps in eps_list:
            # non trec format
#             repeat_rerank(num_exp, alg, eps)
#             repeat_rerank(num_exp, alg, eps, True)

            # trec format
            repeat_rerank_trec(num_exp, alg, eps)
#             repeat_rerank_trec(num_exp, alg, eps, True)

if __name__ == '__main__':
    main()
    
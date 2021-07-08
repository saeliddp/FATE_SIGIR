'''
@author:  ruoyuan
@author: saeliddp
'''
import os
#===============================================================================
# directory
#===============================================================================
homeDir_orig  = os.path.dirname(os.path.realpath(__file__)) + '\\..\\'
homeDir  	  = homeDir_orig + 'bias/'
dataDir  	  = homeDir_orig + 'data/'
rerankDir = dataDir + 'rerank/'
repeat_rerankDir = dataDir + 'repeat_rerank/'
resultDir_google = dataDir + 'results/'

snippetPickle = dataDir + 'snippet.pickle'
snippetFile_original = dataDir + 'scraping_results.txt'

queryDocDir_list = [ dataDir + 'query_docs/q%s/'%i	#starts from 1
					for i in range(1,21)]
                    

for d in queryDocDir_list: 
	if not os.path.exists(d):
		os.makedirs(d)
        
stopword_list = ['abov', 'ani', 'arent', 'becaus', 'befor', 'couldnt', 'didnt', 'doe', 'doesnt', 'dont', 'dure', 'ha', 'hadnt', 'hasnt', 'havent', 'hi', 'isnt', 'mightnt', 'mustnt', 'neednt', 'onc', 'onli', 'ourselv', 'shant', 'shouldnt', 'shouldv', 'thatll', 'themselv', 'thi', 'veri', 'wa', 'wasnt', 'werent', 'whi', 'wont', 'wouldnt', 'youd', 'youll', 'yourselv', 'youv']
stopword_list+= [
    "i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"
]
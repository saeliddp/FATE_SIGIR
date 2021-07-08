import requests
import bs4
import re
import urllib.request
from bs4 import BeautifulSoup
from time import sleep
from random import randint

import sys
import json

blacklist = ['usnews.com', 'nasdaq.com', 'miamiherald.com']
def n_results(query, query_no, file, n=100):
    print("Scraping for: " + query)
    file.write('Query ' + str(query_no) + ' = ' + query)
    query = urllib.parse.quote(query.strip()) # opposite = urllib.parse.unquote()
    
    written_count = 0
    start_num = 1
    unique_results = set()
    
    while (written_count < n):
        print(str(start_num))
        page = urllib.request.urlopen("https://www.bing.com/search?q=" + query + "&first=" + str(start_num))
        soup = BeautifulSoup(page, features="lxml")
        results = soup.find_all("li", class_="b_algo")
        for res in results:
            if (written_count >= n):
                break
                
            try:
                title = "TITLE=" + res.find("h2").find("a").text + "\n"
                
                url = "URL=" + res.find("h2").find("a")["href"] + "\n"
                for domain in blacklist:
                    if domain in url:
                        raise Exception()
                        
                desc = "DESC=" + res.find("p").text + "\n"
                if (title + url + desc) not in unique_results:
                    unique_results.add(title + url + desc)
                    written_count += 1
                    file.write("Rank=" + str(written_count) + "\n")
                    file.write(title)
                    file.write(url)
                    file.write(desc)
                else:
                    print("Duplicate Result")
                
            except:
                print("Missed Result")
        if (len(results) > 0):
            start_num += len(results)
        else:
            print("ZERO LENGTH: " + "https://www.bing.com/search?q=" + query + "&first=" + str(start_num))
            start_num += 1
    
    print("Pausing...")
    sleep(randint(10, 20))
     
if __name__ == "__main__":
    with open("query.txt", "r", encoding="utf-8") as fr:
        queries = fr.readlines()
    
    with open("scraping_results.txt", "w", encoding="utf-8") as fw:
        for i, q in enumerate(queries):
            n_results(q, i + 1, fw)
    
    """
    qid = 1
    with open("results.txt", "w", encoding="utf-8") as fw:
        i = 0
        while (i < len(og_lines)):
            if not og_lines[i].startswith("Topic "):
                i += 1
            else:
                query = og_lines[i][6:]
                fw.write("Query " + str(qid) + " = " + query)
                qid += 1
                ten_results(query, fw)
                fw.write("Rank=11\n")
                for j in range(i + 1, i + 4):
                    fw.write(og_lines[j].replace("[", "").replace("]", ""))
                fw.write("Rank=12\n")
                for j in range(i + 4, i + 7):
                    fw.write(og_lines[j].replace("[", "").replace("]", ""))
                i += 7
                
    """



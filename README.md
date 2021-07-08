# FATE_SIGIR: FATE Online Experimentation Framework

### Contents
1. scraping: code to retrieve rank lists for provided queries  
2. reranking: code to modify rank lists for testing  
3. prepared_data: data used in past experiments (original versus fake news; original versus fairness definitions)  
4. website: full django web app, configured to be deployed on heroku; Currently displays original versus fake news related to COVID-19  

### Workflow
1. Scraping for search engine results:  
	a) Edit scraping/query.txt to contain 20 queries of your own choosing, with one query per line.  
	b) Open scraping/run_this.py. If you want to collect more or less than 100 results per query, edit this parameter in the call to n_results. Note that if you're injecting fake results into rank lists, you likely only need 10 results per query.  
	c) While in scraping directory, run "python3 run_this.py" to initiate the result gathering process. If the script gets stuck on a query, replace that query and start over.  
	d) If you plan to inject fake results into your rank lists, move "results.txt" from the scraping directory to reranking/fake/data. If you plan to rerank based on cluster fairness definitions, move this file to reranking/fairness/data.  
2. Reranking / injecting fake results:  
	a) Follow directions in the parent folder of the folder you just placed "results.txt" into.  
	b) Before moving on to c/d, it would benefit you to go through website/README.md "First time local setup" so you can see the running web app.  
	c) Move the generated <<algorithm.txt>> files to website/version2/txtdata/version2, replacing existing files.  
	d) Move the generated snippet.pickle file to website/version2, replacing existing file  
3. Setting up website:  
	a) Follow directions in website/README.md
# Reranking Based on Fairness Definitions

### Workflow
1. Ensure that data/scraping_results.txt reflects the queries you scraped.
2. While in bias directory, run "python3 generateHIT.py." This script will take a long time to run. Check back periodically to ensure progress.
    a) If script gets stuck on a URL, requests library will eventually time out and the URL will be skipped. The preferable alternative is to add the problematic URL domain to 'blacklist' in scraping/run_this.py and rescrape. If you choose this alternative, ensure that you delete all the contents of ./data/query_docs and replace data/scraping_results.txt before running generateHIT.py again. This process is a weak point of this system--it will likely be frustrating and modifications are welcome.
3. While in bias directory, run "python3 cluster_prep.py"
4. While in bias directory, run "python3 cluster.py"
5. Open bias/rerank.py and edit the main() function to reflect the epsilon levels and rerank algorithm types you wish to test. This is just editing a few lists in main().
6. While in bias directory, run "python3 rerank.py"
7. You'll find the generated txtdata files in data/repeat_rerank/0, and snippet.pickle will be in data directory.
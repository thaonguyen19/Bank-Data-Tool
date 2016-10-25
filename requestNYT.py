import requests
import json
import time #delay the retrieval of data so as not to exceed API rate limit
import urllib.request
from bs4 import BeautifulSoup

key = "cb2cf4f67d0245689fa8b1921c912f2a"
base_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
word_list = ['bank']
#resp = requests.get(base_url + "?q=bank&fq=section_name:Business&api-key="+key)

all_articles=[] #list of all the articles found
for word in word_list:
	for page in range(0,10): #can increase to 100, as long as check status_code before execution
		search_params = {"q" : "bank", 
						"fq" : ["source: The New York Times","section_name: Business"],
						"page": page,
						"api-key" : key}
		resp = requests.get(base_url, params = search_params)
		if (resp.status_code == 200):
			resp = resp.json()
			response = resp['response']['docs']
			all_articles = all_articles + response
			time.sleep(2)
		
print (len(all_articles)) #total number of articles found so far
		
		

all_articles = all_articles[:1] #testing with one article first
for article in all_articles:
	print (article['web_url'])
	article_page = urllib.request.urlopen(article['web_url']) #open the url of the article
	soup = BeautifulSoup(article_page.read()) #convert it into an html element
	print (soup(itemprop="articleBody")) #find all the relevant news content, marked with "articleBody" tag
	time.sleep(2)



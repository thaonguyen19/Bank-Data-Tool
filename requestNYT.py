import requests
import json
import time #delay the retrieval of data so as not to exceed API rate limit
import urllib
import csv
#from bs4 import BeautifulSoup

key = "cb2cf4f67d0245689fa8b1921c912f2a"
key2 = "071b39978a18407489be0dcf0cbf9697"
base_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
word_list = ['bank', 'market', 'losses', 'crisis', 'finance', 'financial', 'law', 'downturn', 'credit']

articles_collection = {} #dictionary to store year and articles found in that year

for year in range(2000, 2016):
	testfile = open('Year' + str(year) + '.csv', 'w')
	f = csv.writer(testfile)
	f.writerow(['Headline', 'URL', 'ID', 'Print page', 'Word count', 'Pub date', 'Lead paragraph', 'Abstract'])
	print ("year: ", year)	
	yearly_articles= [] #list of all the articles found for a certain year
	articles_id = set() #keep check of all articles that have been added to avoid duplicates
	for word in word_list:
		for page in range(0,100): #can increase to arbitrary amount, as long as check status_code before execution
			begin_date= str(year) + "0101"
			end_date = str(year) + "1231"
			search_params = {"q" : word, 
							"fq" : ["source: The New York Times","section_name: Business"],
							"page": page,
							"begin_date": begin_date,
							"end_date": end_date,
							"api-key" : key}
			resp = requests.get(base_url, params = search_params)
			if (resp.status_code == 200):
				resp = resp.json()
				response = resp['response']['docs']
				for article in response[0:2]: #iterate through each article in the result returned
					print (article)
					if article['_id'] not in articles_id: #if article has not been added to the collection
						articles_id.add(article['_id'])
						yearly_articles.append(article)
						f.writerow([article['headline']['main'], article['web_url'], article['_id'],
								article['print_page'], article['word_count'], article['pub_date'], 
								article['lead_paragraph'], article['abstract']])
			time.sleep(1)
	articles_collection[year] = yearly_articles
	print (len(articles_collection[year])) #total number of articles found for a year
	testfile.close()
		
		
#TO RETRIEVE CONTENT FOR AN ARTICLE
#all_articles = all_articles[:1] #testing with one article first
# for i in range(len(all_articles)):
# 	article = all_articles[i]
# 	print ("index: ", i)
# 	article_page = urllib.request.urlopen(article['web_url']) #open the url of the article
# 	soup = BeautifulSoup(article_page.read()) #convert it into an html element
# 	print (soup(itemprop="articleBody")) #find all the relevant news content, marked with "articleBody" tag




import requests
import json
import urllib
import csv
 
### Some fields are often missing (eg. section_name, headline): hard to filter articles relevant to business
### But run faster than direct article search

#YEAR 1925-2016

key = "cb2cf4f67d0245689fa8b1921c912f2a"
key2 = "071b39978a18407489be0dcf0cbf9697"
base_url_start = "http://api.nytimes.com/svc/archive/v1/" #+year
base_url_end = "/1.json?api-key=" #+api
word_list = ['bank', 'market', 'losses', 'crisis', 'finance', 'financial', 'law', 'downturn', 'credit']

articles_collection = {} #dictionary to store year and articles found in that year

for year in range(2015, 2017):
	base_url = base_url_start + str(year) + base_url_end + key2
	testfile = open('Year' + str(year) + '.csv', 'w')
	f = csv.writer(testfile)
	f.writerow(['Headline', 'URL', 'ID', 'Print page', 'Word count', 'Pub date', 'Section name','Lead paragraph', 'Abstract'])
	print ("year: ", year)	
	yearly_articles= [] #list of all the articles found for a certain year
	resp = requests.get(base_url)
	if (resp.status_code == 200):
		resp = resp.json()
		response = resp['response']['docs']
		for article in response:
			print(article)
			for word in word_list:
				if ((len(article['headline']) != 0 and 'main' in article['headline'].keys() and word in article['headline']['main'])
					or (article['lead_paragraph'] is not None and word in article['lead_paragraph']) 
					or(article['abstract'] is not None and word in article['abstract'])):
					yearly_articles.append(article)
					f.writerow([article['headline']['main'], article['web_url'], article['_id'],
								article['print_page'], article['word_count'], article['pub_date'], 
								article['section_name'], article['lead_paragraph'], article['abstract']])
					break 

		print (len(yearly_articles))

	testfile.close()

 
		
 



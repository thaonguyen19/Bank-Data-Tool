#import requests
from nytimesarticle import articleAPI
api = articleAPI('cb2cf4f67d0245689fa8b1921c912f2a')
#articles = requests.get("")
articles = api.search( q = 'bank', 
	fq = {'source':'The New York Times', 'section_name': 'Business'}, #filter using dictionary and list for multiple items in each category
    begin_date = 20001231 )
print ('hello')

def parse_articles(articles):
    '''
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    '''
    news = []
    for i in articles['response']['docs']:
        dic = {}
        dic['id'] = i['_id']
        if i['abstract'] is not None:
            dic['abstract'] = i['abstract'].encode("utf8")
        dic['headline'] = i['headline']['main'].encode("utf8")
        dic['desk'] = i['news_desk']
        dic['date'] = i['pub_date'][0:10] # cutting time of day.
        dic['section'] = i['section_name']
        if i['snippet'] is not None:
            dic['snippet'] = i['snippet'].encode("utf8")
        dic['source'] = i['source']
        dic['type'] = i['type_of_material']
        dic['url'] = i['web_url']
        #dic['word_count'] = i['word_count']
        #locations = []
        #for x in range(0,len(i['keywords'])):
        #    if 'glocations' in i['keywords'][x]['name']:
        #        locations.append(i['keywords'][x]['value'])
        #dic['locations'] = locations
        subjects = []
        for x in range(0,len(i['keywords'])):
            if 'subject' in i['keywords'][x]['name']:
                subjects.append(i['keywords'][x]['value'])
        dic['subjects'] = subjects   
        news.append(dic)
    return(news) 
    end


def get_articles(date,query):
    '''
    This function accepts a year in string format (e.g.'1980')
    and a query (e.g.'Amnesty International') and it will 
    return a list of parsed articles (in dictionaries)
    for that year.
    '''
    all_articles = []
    for i in range(0,1): #NYT limits pager to first 100 pages. 
        articles = api.search(q = query,
               fq = {'source':'The New York Times', 'section_name':'Business'},
               begin_date = date + '0101',
               end_date = date + '1231',
               sort='oldest',
               page = str(i))
        articles = parse_articles(articles)
        all_articles = all_articles + articles
    return(all_articles)

Bank_all = []
for i in range(1980,2014):
	print ('Processing' + str(i) + '...')
bank_by_year =  get_articles(str(i),'Bank')
Bank_all = Bank_all + bank_by_year
print (Bank_all)

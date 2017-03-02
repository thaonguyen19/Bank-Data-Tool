#!/usr/bin/env python

"""Web scraper application for nytimes.com.

This program searches nytimes.com for posts that contain certain given keywords.
"""

import datetime                     
import time
import requests
import json
#from bs4 import BeautifulSoup      


# twilio constants
TWILIO_ACCOUNT_SID = "AC2469612ba4f5ace2e091a99807274140"
TWILIO_AUTH_TOKEN = "c85a1f493ef92261e290b86f345c66bd"
MY_PHONE_NUMBER = "+16504712300"
TWILIO_PHONE_NUMBER = "+14083530602"

#other constants
NYT_KEY = "071b39978a18407489be0dcf0cbf9697"
LINK = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
KEYWORDS = ["machine learning", "AI"]
DAYS_OFFSET = 3 # number of days back to search for keywords

SENT_POSTS = [] #keep track of what has been sent to avoid duplicates
SLEEP_TIME = 30 

def main():
    while True:
        print("Scraping data from nytimes.com for keywords {0}...".format(", ".join(KEYWORDS)))
        matches = scrape_post(KEYWORDS, LINK, DAYS_OFFSET)
        print("Done scraping.")
        if len(matches) > 0:
            notify_sms(KEYWORDS, matches)

        time.sleep(SLEEP_TIME)


def notify_sms(keywords, matches):
    tosend = [] #list of links to send
    for match in matches:
        if match[0] not in SENT_POSTS: #if link has not been sent before
            tosend.append(match[0])
            SENT_POSTS.append(match[0])
    if len(tosend) > 0:
        print("Found {0} new post(s)!".format(len(tosend)))
        # content of text message
        body = "Scraper found {0} post(s) about {1} in nytimes: \n\n".format(len(tosend), ", ".join(keywords))
        body += "\n".join(tosend)
        endpoint = "https://api.twilio.com/2010-04-01/Accounts/{0}/Messages.json".format(TWILIO_ACCOUNT_SID)
        data = {"To": MY_PHONE_NUMBER,
                "From": TWILIO_PHONE_NUMBER,
                "Body": body}
        r = requests.post(endpoint, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), data=data)
        try:
            tr = json.loads(r.text)
            if tr["status"] == "failed" or tr["status"] == "undelivered":
                print("Unable to send text message: Twilio reported failed or undelivered.")
        except Exception(e):
                print("Unable to send text message: Invalid response by Twilio API.")

def scrape_post(keywords, link, days_to_check):
    """Scrapes the given link to find all posts that contain the given keywords.
    Args:
        keywords (list of str): keywords to search for.
        link: link to scrape.
        days_to_check (int): number of days back to search.
    Returns:
        A list of matches where each match is a tuple of link and post title.
    """
    print ("Scraping " + link + " in progress ...")
    oldest_date = (datetime.date.today() -
                   datetime.timedelta(days=days_to_check))
    oldest_date_str = oldest_date.strftime("%Y%m%d")
    today_date_str = datetime.date.today().strftime("%Y%m%d")

    matches = []
    for word in KEYWORDS:
        for page in range(0,10):  
            search_params = {"q" : word, 
                            "fq" : ["source: The New York Times"],
                            "page": page,
                            "begin_date": oldest_date_str,
                            "end_date": today_date_str,
                            "api-key" : NYT_KEY}
            resp = requests.get(LINK, params = search_params)
            if (resp.status_code == 200):
                resp = resp.json()
                response = resp['response']['docs']
                for article in response: #iterate through each article in the result returned
                    matches.append((article['web_url'], article['headline']['main']))
                    
            time.sleep(3)

    print (matches)
    return matches
    

if __name__ == "__main__":
    main()

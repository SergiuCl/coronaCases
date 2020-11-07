from newsapi import NewsApiClient
import http.client
import json


def get_news():

    # get a news API
    newsapi = NewsApiClient(api_key="ac881b4ffacf4b37a3d574832e6653c5")
    # get the top headlines from API
    topheadlines = newsapi.get_top_headlines(q='corona', language='de', country="at")
    
    # save the articles variables
    articles = topheadlines['articles']
    desc = []
    news = []
    img = []
    content = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        content.append(myarticles['content'])
    
    mylist = zip(news, desc, img, content)
    return mylist


def get_dict_news():
    # get a news API
    newsapi = NewsApiClient(api_key="ac881b4ffacf4b37a3d574832e6653c5")
    # get the top headlines from API
    topheadlines = newsapi.get_top_headlines(q='corona', language='de', country="at")
    #print(topheadlines)
    # save the articles variables
    articles = topheadlines['articles']
    return articles



def get_API_News_austria():

    # HTTP Client Corona URL
    conn = http.client.HTTPSConnection("covid-19-tracking.p.rapidapi.com")

    # set headers
    headers = {
        'x-rapidapi-host': "covid-19-tracking.p.rapidapi.com",
        'x-rapidapi-key': "a3319b5d01msh92069bd8db5f8d8p170d8bjsnc4e22ecc8609"
    }

    # get the cases from Austria
    conn.request("GET", "/v1/austria", headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    # load the data in JSON
    casesAustria = json.loads(data)

    return casesAustria


def get_API_News_world():

    # HTTP Client Corona URL
    conn = http.client.HTTPSConnection("covid-19-tracking.p.rapidapi.com")
    
    # set headers
    headers = {
        'x-rapidapi-host': "covid-19-tracking.p.rapidapi.com",
        'x-rapidapi-key': "a3319b5d01msh92069bd8db5f8d8p170d8bjsnc4e22ecc8609"
        }

    conn.request("GET", "/v1", headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    # load the data in JSON
    casesWorld = json.loads(data)

    return casesWorld


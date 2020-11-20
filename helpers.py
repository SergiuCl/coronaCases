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
    casesWorld = json.loads(data.decode('utf-8'))

    return casesWorld


def convert_to_int(str):
    
    """ check if str is empty or N/A
    if yes, return an empty string
    else replace comma with space and convert the str into an int """
    if not str or str == "N/A":
        s = ''
        return s
    else:
        s = str.replace(",", "")

        if "+" in s:
            s.replace("+" , "")

        i = int(s)

    return i


# define a function to get the data from SQLite3 in dict instead of tuple
def dict_factory(cursor, row):

    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# define a function to append the data from querys to a list
def get_value_list(data, dictKey):

    result = []
    for i in range(len(data)):
        result.append(data[i][dictKey])
    return result
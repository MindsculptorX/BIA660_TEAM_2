# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 15:00:40 2017

@author: Yi Zhao
"""

from bs4 import BeautifulSoup
import re
import time
import requests
import pandas as pd
import os

def get1(div_review, classdesc):
    try:
        li_friends = div_review.findAll('li', {'class': classdesc})
        li_friends_b = li_friends[0].findAll('b')
        friends = li_friends_b[0].contents[0]
        return friends
    except:
        return 0


def analyseHtml(html, rId):
    results = []
    print(rId)

    soup = BeautifulSoup(html,'lxml') # parse the html 
    reviews=soup.findAll('div',{'class':'review review--with-sidebar'})
    
    for div_review in reviews:
        result = {'restaurantId': rId}
        
        review_id = div_review['data-review-id']
        result['review_id'] = review_id

        try:
            a_username = div_review.findAll('a', {'class': 'user-display-name js-analytics-click'})
            username = a_username[0].contents[0]
            result['username'] = username
        except IndexError:
            result['username'] = ''
        
        num_friends = get1(div_review, 'friend-count responsive-small-display-inline-block')
        result['num_friends'] = num_friends
        num_reviews = get1(div_review, 'review-count responsive-small-display-inline-block')
        result['num_reviews'] = num_reviews
        num_photos = get1(div_review, 'photo-count responsive-small-display-inline-block')
        result['num_photos'] = num_photos
        
        try:
            review_text = div_review.findAll('p', {'lang': 'en'})[0].contents[0]
            result['review_text'] = review_text
        except IndexError:
            result['review_text'] = ''
        
        rating_qualifier = div_review.findAll('span', {'class': 'rating-qualifier'})[0].contents[0]
        result['date'] = rating_qualifier.strip()
        
        elite = len(div_review.findAll('a', {'href': '/elite'}))
        result['elite'] = elite
        
#        useful = div_review.findAll('p', {'class': 'voting-intro voting-prompt saving-msg'})[0].contents[0]
        try:
            a_useful = div_review.findAll('class', {'ybtn ybtn--small useful js-analytics-click'})[0]
            span_useful = a_useful.findAll('span', {'class': 'count'})[0]
            useful = span_useful.contents[0]
            result['useful'] = useful
        except IndexError:
            result['useful'] = 0
        
        rating = div_review.findAll('div', {'class': 'rating-large'})[0]['title']
        result['rating'] = rating.split()[0]
    
        results.append(result)
        
    return results

def analyseDir(path, rId):
    csvfilepath = os.path.join(path, 'data.csv')
    if os.path.isfile(csvfilepath) == True:
        return pd.read_csv(csvfilepath)
    else:
        res = []
        tempfilepath = 'temp.csv'
        f = open(os.path.join(path, 'metadata'))
        pages = int(f.readlines()[3])
        for page in range(pages):
            res += analyseHtml(open(os.path.join(path, str(page) + '.html')).read(), rId)
        df2 = pd.DataFrame(res)
        df2.to_csv(tempfilepath)
        os.rename(tempfilepath, csvfilepath)
        return df2

#print(analyseDir('/Users/enyaning/Desktop/BIA660/BIA660_TEAM_2/chinese_0/'))

def analyseGene(name, max_id):
    dfs = []
    for id in range(max_id + 1):
        df = analyseDir('/Users/enyaning/Desktop/BIA660/BIA660_TEAM_2/' + name + '_' + str(id), name + '_' + str(id))
        dfs.append(df)
    return pd.concat(dfs)

def main(name, max_id):
    df2 = analyseGene(name, max_id)
    df2.to_csv(name + '.csv')

if __name__ == '__main__': 
    main('mexican', 50)
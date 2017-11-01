# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 15:00:40 2017

@author: He Song
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


def analyseHtml(html):
    results = []


    soup = BeautifulSoup(html,'lxml') # parse the html 
    reviews=soup.findAll('div',{'class':'review review--with-sidebar'})
    
    for div_review in reviews:
        result = {}
        
        review_id = div_review['data-review-id']
        result['review_id'] = review_id

        a_username = div_review.findAll('a', {'class': 'user-display-name js-analytics-click'})
        username = a_username[0].contents[0]
        result['username'] = username
        
        num_friends = get1(div_review, 'friend-count responsive-small-display-inline-block')
        result['num_friends'] = num_friends
        num_reviews = get1(div_review, 'review-count responsive-small-display-inline-block')
        result['num_reviews'] = num_reviews
        num_photos = get1(div_review, 'photo-count responsive-small-display-inline-block')
        result['num_photos'] = num_photos
        
        review_text = div_review.findAll('p', {'lang': 'en'})[0].contents[0]
        result['review_text'] = review_text
        
        rating_qualifier = div_review.findAll('span', {'class': 'rating-qualifier'})[0].contents[0]
        result['date'] = rating_qualifier.strip()
        
        results.append(result)
        
    return results

def analyseDir(path):
    with open(os.path.join(path, 'metadata')) as f:
        res = []
        pages = int(f.readlines()[3])
        for page in range(pages):
            res += analyseHtml(open(os.path.join(path, str(page) + '.html')).read())
    return res

#print(analyseDir('/Users/enyaning/Desktop/BIA660/BIA660_TEAM_2/chinese_0/'))

def analyseGene(name, max_id):
    res = []
    for id in range(max_id + 1):
        res += analyseDir('/Users/enyaning/Desktop/BIA660/BIA660_TEAM_2/' + name + '_' + str(id))
    return res

def main(name, max_id):
    jsonarray = analyseGene(name, max_id)
    df2 = pd.DataFrame(jsonarray)
    df2.to_csv(name + '.csv')

if __name__ == '__main__': 
    main('chinese', 0)
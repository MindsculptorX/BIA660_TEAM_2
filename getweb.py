# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 15:00:40 2017

@author: He Song
"""

from bs4 import BeautifulSoup
import re
import time
import requests

def reviews(url,type):
    for p in range(1,10):
        pageLink=url+'/search?find_loc=Los+Angeles,+CA&start='+str(p*10)+'&cflt=' +type# make the page url
        for i in range(5): # try 5 times
                    try:
                        #use the browser to access the url
                        response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                        html=response.content # get the html
                        break # we got the file, break the loops
                    except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                        print ('failed attempt',i)
                        time.sleep(2) # wait 2 secs
        				
        		
        if not html:continue # couldnt get the page, ignore
                
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 
        divget=soup.findAll('div',{'class':'media-story'})
        
        for div in divget:
            #print(review)
            #print(div)
            restaurant=div.find('a', {'class':'biz-name js-analytics-click'}) # get all the review divs
            kind=div.find('span',{'class':'category-str-list'})
            #print(restaurant)
           
            if restaurant:
                if 'ad_business_id' not in restaurant['href']:
                    kind_s=kind.findAll('a')
                    if len(kind_s)==1:
                        
                        reviewnum=div.find('span',{'class':'review-count rating-qualifier'})
                        
                        reviewnum=reviewnum.text.replace('reviews','')
                        reviewnum=reviewnum.replace(' ','')
                        if int(reviewnum)>200 :
                        #print(kind)
                            print(reviewnum)
                            nextse=restaurant['href']
                            print(nextse)
                            sp=restaurant.find('span')
                            print(sp.text)
                            print('\n')
                    
                    
reviews('https://www.yelp.com','chinese')
from bs4 import BeautifulSoup
import re
import time
import requests
import os
def gethtml(filename):
    newdir = filename[:-4]
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip().split('\t') for x in content] 
    namelist = {}
    for i in content:
        if len(i)==2:
            namelist[i[1]] = i[0]
    for name,url_piece in namelist.items():
        subdir = name
        if not os.path.exists(subdir):
            os.makedirs(newdir+'/'+subdir)
        url = 'https://www.yelp.com'+url_piece
        for i in range(5): 
            try:

                response=requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content 
                break 
            except Exception as e:
                print ('failed attempt',i)
                time.sleep(2) 
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
        pages=soup.findAll('div', {'class':re.compile('page-of-pages')})
        pageNum = int(re.findall(r'of \d{0,5}', str(pages[0]))[0][3:])

        for p in range(1,pageNum+1): 
            fw=open(newdir+'/'+subdir+'/'+'page'+str(p)+'.txt','w')

            print ('page',p)
            html=None

            if p==1: pageLink=url # url for page 1
            else: pageLink=url+'?start='+str((p-1)*20) # make the page url

            for i in range(5): # try 5 times
                try:
                    #use the browser to access the url
                    response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                    html=response.content # get the html
                    break # we got the file, break the loop
                except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                    print ('failed attempt',i)
                    time.sleep(1) # wait 2 secs
                if not html:continue # couldnt get the page, ignore
            soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
            fw.write(soup.prettify())
            fw.close()
#gethtml('chinese.txt')
#gethtml('mexican.txt')
#gethtml('italian.txt')




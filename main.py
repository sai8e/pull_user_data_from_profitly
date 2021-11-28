import re
import concurrent.futures
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from trade import getInfoFrom, writeToCvs
import re

begin_time = datetime.datetime.now()

user = 'Jackaroo'


count=1

def getNumOfPages():
    URL = 'https://profit.ly/user/%s/trades' % (user)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find('div', attrs={'class': 'input-group-append'}).findChild().text[3:]


lastPageNum = int(re.sub("[^0-9]", "", getNumOfPages()))
print(lastPageNum)
# lastPageNum = 1

for i in range(1, lastPageNum+1, 1):
    
    print("page: ", i)
    URL = 'https://profit.ly/user/%s/trades?page=%s&size=10' % (user, i)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    newList=[]

    for l in soup.find_all('a', class_=re.compile('^trade-')):
        link = l.get('href')
        if not 'ticker' in link:
            newList.append("https://profit.ly/" + link)

    # newList.reverse()

    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(getInfoFrom, newList)
    
    # for individualTrade in newList:
    #     print("trade: ", count, " ", individualTrade)
    #     getInfoFrom(individualTrade)
    #     count +=1 
    
writeToCvs(user)
print(datetime.datetime.now() - begin_time)


import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

date_arr=[]
ticker_arr=[]
tradeType_arr=[]
entry_arr=[]
exit_arr=[]
position_arr=[]
profit_arr=[]
percentage_arr=[]
entryDate_arr=[]
exitDate_arr=[]
brokers_arr=[]
comment_arr=[]


def getInfoFrom(individualTrade):

    date = "N/A"
    ticker = "N/A"
    tradeType ="N/A" 
    entry ="N/A"
    exit ="N/A"
    position ="N/A"
    profit="N/A"
    percentage="N/A"
    entryDate="N/A"
    exitDate="N/A"
    brokers="N/A"
    comment="N/A"
    

    page = requests.get(individualTrade)
    soup = BeautifulSoup(page.content, 'html.parser')

    date = soup.find('date').text
    ticker = soup.find('a', attrs={'class': 'trade-ticker'}).text
    tradeType = soup.find('span', attrs={'class': 'trade-type'}).text.split()[0] 
    data = []
    try: 
        for row in soup.find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text for ele in cols]
            data.append(cols)
        
        entryDate = data[1][1]
        entry = data[1][2]

        exitDate = data[2][1]
        exit = data[2][2]
    except AttributeError:
        entry = "N/A"
        exit = "N/A"
    try:
        profit = soup.find('a', class_=re.compile('^trade-')).text.split()[0]
    except AttributeError:
        profit = "N/A"
    
    for ele in soup.findAll('li', attrs={'class': 'list-group-item'}):
        if('Position Size' in ele.text): 
            position= ele.find('span').text
        if('Percentage' in ele.text): 
            percentage=ele.find('span').text.strip()

    try:
        broker = soup.find('a', href=re.compile('^/broker/')).text
    except AttributeError:
        broker = "N/A"

    try:
        comment = soup.find('p', attrs={'class': 'wall-text'}).text
    except AttributeError:
        comment = "N/A"    

    date_arr.append(date)
    ticker_arr.append(ticker)
    tradeType_arr.append(tradeType)
    entry_arr.append(entry)
    exit_arr.append(exit)
    position_arr.append(position)
    profit_arr.append(profit)
    percentage_arr.append(percentage)
    entryDate_arr.append(entryDate)
    exitDate_arr.append(exitDate)
    brokers_arr.append(broker)
    comment_arr.append(comment)


def writeToCvs(user):
    d = {'Date': date_arr,
    'Ticker': ticker_arr,
    'Trade Type': tradeType_arr,
    'Entry': entry_arr,
    'Exit': exit_arr,
    'Position Size': position_arr,
    'Profit': profit_arr,
    'Percentage': percentage_arr,
    'EntryDate': entryDate_arr,
    'ExitDate': exitDate_arr,
    'Broker': brokers_arr,
    'Comment': comment_arr}
    df = pd.DataFrame.from_dict(d, orient='index')
    df = df.transpose() 

    df.to_csv('./trades/'+user+'.csv', index=False, encoding='utf-8')

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import pickle

driver=webdriver.Chrome(r'C:\Users\aryan\Downloads\chromedriver_win322/chromedriver.exe')
userArray=np.array([])
movieArray=np.array([])
scoreArray=np.array([])


#load in topAnime.csv
topAnime=pd.read_csv('pholderAnime.csv')

urlprefix='https://myanimelist.net/animelist/'
urlpostfix='?status=7'


def getAnimeList(user):
    global userArray
    global movieArray
    global scoreArray
    url=urlprefix+user+urlpostfix
    #check if url is valid
    if not validURL(url):
        return
    search=driver.find_elements(By.CLASS_NAME,'list-table-data')
    for element in search:
        soup=BeautifulSoup(element.get_attribute('innerHTML'),'html.parser')
        name=soup.find_all('a')[0]['href'].split('/')[3]
        #replace every '-' with ' ' in name
        name=name.replace('_',' ')
        #if the name is not in topAnime.csv, then skip it
        if name not in topAnime['movieName'].values:
            continue
        finaldk=(soup.find_all('span', attrs={'class': re.compile("^score-label score-[0-9]")}))
        if len(finaldk)==0:
            continue
        score=int(finaldk[0].text.strip())
        userArray=np.append(userArray,user)
        movieArray=np.append(movieArray,name)
        scoreArray=np.append(scoreArray,score)
def validURL(url):
    driver.get(url)
    search=driver.find_elements(By.CLASS_NAME, 'badresult')
    if len(search)!=0:
        return False
    return True
#load in users.pickle
users=[]
with open('1.pickle','rb') as f:
    users=pickle.load(f)
def getAnimeLists():
    for i in range(len(users)):
        getAnimeList(users[i])
        print(i)
getAnimeLists()
#save userArray, movieArray, scoreArray into a dataframe
df=pd.DataFrame({'user':userArray,'movie':movieArray,'score':scoreArray})
df.to_csv('ratings1.csv',index=False)
print(df.head())




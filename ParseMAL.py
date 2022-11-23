import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re

driver=webdriver.Chrome(r'C:\Users\aryan\Downloads\chromedriver_win322/chromedriver.exe')
score_chart=[]

url='https://myanimelist.net/animelist/Ryuseishun?status=7'


def getAnimeList(url):
    driver.get(url)
    time.sleep(1)
    search=driver.find_elements(By.CLASS_NAME,'list-table-data')
    for element in search:
        soup=BeautifulSoup(element.get_attribute('innerHTML'),'html.parser')
        name=soup.find_all('a')[0]['href'].split('/')[3]
        #replace every '-' with ' ' in name
        name=name.replace('_',' ')
        finaldk=(soup.find_all('span', attrs={'class': re.compile("^score-label score-[0-9]")}))
        if len(finaldk)==0:
            continue
        score=int(finaldk[0].text.strip())
def validURL(url):
    driver.get(url)
    time.sleep(1)
    search=driver.find_elements(By.CLASS_NAME, 'badresult')
    if len(search)!=0:
        return False
    return True

getAnimeList(url)
print(validURL(url))


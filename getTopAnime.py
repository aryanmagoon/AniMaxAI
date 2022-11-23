from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import numpy as np

currMovieID=1



driver=webdriver.Chrome(r'C:\Users\aryan\Downloads\chromedriver_win322/chromedriver.exe')
#create identical second driver
#driver2=webdriver.Chrome(r'C:\Users\aryan\Downloads\chromedriver_win322/chromedriver.exe')

base_url='https://myanimelist.net/topanime.php?limit='

#create three np arrays to store movieID, movie name, and movie genres
movieID=np.array([])
movieName=np.array([])
movieLinks=np.array([])
#make movieTags np array
movieTags=np.array([])




def getGenresFromAnime():
    global movieLinks
    global movieTags
    for i in movieLinks:
        driver.get(i)
        genstring=""
        search=driver.find_elements(By.CLASS_NAME,'spaceit_pad')
        for element in search:
            soup=BeautifulSoup(element.get_attribute('innerHTML'),'html.parser')
            #find all span in soup
            span=soup.find_all('span')
            
            isGenres=False
            for i in range(len(span)):
                if i==0 and span[i].text.strip()=='Genres:':
                    isGenres=True
                    continue
                if isGenres:
                    genstring+=span[i].text.strip()+"|"
        movieTags=np.append(movieTags,genstring[:-1])
                    
def getAnimeFromPage(page_number):
    global currMovieID
    global movieID
    global movieName
    global movieLinks
    url=base_url+str(page_number)
    driver.get(url)
    #search=driver.find_elements(By.CLASS_NAME,'hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3')
    #find element by css selector
    search=driver.find_elements(By.CSS_SELECTOR,'.hoverinfo_trigger.fl-l.fs14.fw-b.anime_ranking_h3')
    for anime in search:
        soup=BeautifulSoup(anime.get_attribute('innerHTML'),'html.parser')
        a_tag=soup.find_all('a')[0]
        name=a_tag.text.strip()
        href=a_tag['href']
        #add to np arrays
        movieID=np.append(movieID,currMovieID)
        movieName=np.append(movieName,name)
        movieLinks=np.append(movieLinks,href)
        currMovieID+=1
def getTopAnime(num_entries):
    for i in range(0,num_entries+50,50):
        getAnimeFromPage(i)



#getAnimeFromPage(0)
#getGenresFromAnime()
#sgetAnimeFromPage(0)
#print the np arrays
#create a dataframe out of the np arrays
getTopAnime(13300)
getGenresFromAnime()
import pandas as pd
df=pd.DataFrame({'movieID':movieID,'movieName':movieName,'movieLinks':movieLinks, 'movieTags':movieTags})
#make movieID into type int
df['movieID']=df['movieID'].astype(int)
#save df to a csv
df.to_csv('topAnime.csv',index=False)

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

driver=webdriver.Chrome(r'C:\Users\aryan\Downloads\chromedriver_win322/chromedriver.exe')

users=[]



def getUsers():
    global users
    driver.get('https://myanimelist.net/users.php')
    time.sleep(1)
    search=driver.find_elements(By.CLASS_NAME,'borderClass')
    for element in search:
        soup=BeautifulSoup(element.get_attribute('innerHTML'),'html.parser')
        username=soup.find_all('a')[0].text.strip()
        if(username not in users):
            users.append(username)
def scrapeUsers():
    global users
    timewithoutchange=0
    prevlen=len(users)
    while(timewithoutchange<50 or len(users)<100000):
        getUsers()
        if(prevlen==len(users)):
            timewithoutchange+=1
        else:
            timewithoutchange=0
        prevlen=len(users)
        #print prevlen and timewithout change with identifiers
        print("amount of users"+str(prevlen))
        print("iterations without change"+str(timewithoutchange))

scrapeUsers()


#save users into a pickle file
import pickle
def saveUsers():
    global users
    with open('users.pickle','wb') as f:
        pickle.dump(users,f)
def loadUsers():
    global users
    with open('users.pickle','rb') as f:
        users=pickle.load(f)
saveUsers()


    
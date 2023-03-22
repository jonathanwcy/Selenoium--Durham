from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import time
import csv
import pandas as pd

from bs4 import BeautifulSoup
import requests

#Define Executable Path
options=Options()
options.chrome_executable_path= "/usr/local/bin/chromedriver"
driver=webdriver.Chrome(options=options)

def turnon(link):
    try:
        driver.get(link)
    except:
        print('no internet access')

#Open URL
def OpenCategory():
    turnon('https://opendata.durham.ca/')
    time.sleep(5)
    driver.maximize_window()
    # Count number of categories
    clas=driver.find_elements(By.CLASS_NAME,"category-card")
    length=len(clas)


    # while loop for clicking differenet categories
    count=0
    while (count<length):
        find= driver.find_elements(By.CLASS_NAME,"category-card")
        time.sleep(5)    
        find[count].click()
        time.sleep(5)
        results= driver.find_elements(By.XPATH,"//*[@id='search-results']/li")

        #While loop for clicking each file under each categories
        i=0
        while (i<=len(results)):
            id="search-result-element-id-"+str(i)
            Boolean= driver.find_elements(By.ID,id)
            if len(Boolean)>0:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, id))).click()
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "View Full Details"))).click()

                #Capturing the Summary
                sum=driver.find_element(By.CLASS_NAME,"overflow-toggle-inner")
                title=driver.find_element(By.CLASS_NAME, "content-hero-header").text
                s= open(title + '_Summary.txt','w')
                s.write(sum.text)


                #Capturing the Attribute Table
                driver.maximize_window()
                time.sleep(5)
                Read_more= driver.find_elements(By.XPATH, "//*[@id='main-region']/div[3]/div/div/div[1]/div[4]/div/button")
                if len(Read_more)>0:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main-region']/div[3]/div/div/div[1]/div[4]/div/button"))).click()
                    page_source=driver.page_source
                    soup= BeautifulSoup(page_source,'lxml')
                    table=soup.find('table', attrs={'class':'table table-striped'} )
                    df=pd.read_html(str(table))
                    title=driver.find_element(By.CLASS_NAME, "content-hero-header").text
                    df[0].to_csv(title + '_Attributes.csv',index=False)
                else: 
                    page_source=driver.page_source
                    soup= BeautifulSoup(page_source,'lxml')
                    table=soup.find('table', attrs={'class':'table table-striped'} )
                    df=pd.read_html(str(table))
                    title=driver.find_element(By.CLASS_NAME, "content-hero-header").text
                    df[0].to_csv(title + '_Attributes.csv',index=False)

                #Capturing the Tags
                driver.maximize_window()
                time.sleep(5)
                li=driver.find_elements(By.XPATH, "//*[@id='main-region']/div[3]/div/div/div[3]/div[3]/ul")
                for tags in li:
                    print ('')
                title=driver.find_element(By.CLASS_NAME, "content-hero-header").text
                t1= open(title+'_Tags.txt','w')
                t1.write(tags.text)


                driver.back()
                time.sleep(5)
                driver.back()

                time.sleep(5)
                i+=1
            else:
                i+=1
       
        driver.get('https://opendata.durham.ca/')
        time.sleep(10)
        count+=1
    
    else:
        print('Test Complete')


OpenCategory()


driver.close()

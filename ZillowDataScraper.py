#!/usr/bin/env python
# coding: utf-8

# Webscraping Zillow


import requests
from time import strftime
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from secrets import Secrets


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}


url = 'https://www.zillow.com/homes/for_rent/Manhattan,-New-York,-NY_rb'


html = requests.get(url=url,headers=HEADERS)

driver = webdriver.Chrome(service=Service(Secrets.CHROME_DRIVER_PATH),)
driver.get(url)

# bsobj = soup(html.content,'html.parser')
bsobj = soup(driver.page_source,'html.parser')

price_list = []

for price in bsobj.findAll('div',{'class':'list-card-heading'}):
    # print('price is: ', price.text.replace('bd','b|').replace('|s','|').replace('io','io|').strip().split('|')[:-1])
    parsedLst = price.text.replace('bd','b|').replace('|s','|').replace('o','o|').strip().split('|')[:-1]
    if parsedLst:
        price_list.append(parsedLst)


address = []

for adr in bsobj.findAll('address',{'class':'list-card-addr'}):
    address.append(adr.text.strip())

import pandas as pd

df = pd.DataFrame(price_list,columns=['Price1','Price2','Price3',])
df['Address'] = address

driver.quit()

df.to_csv(f"data/data_{strftime('%Y-%m-%d-%H-%M-%S')}.csv")






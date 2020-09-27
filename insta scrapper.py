# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 11:02:37 2020

@author: Prince
"""

#Open the web browser: Selenium uses chrome driver to open the profile given a username (public user). For example 
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np



username='pickuplines'
browser = webdriver.Chrome(r'C:\Users\Prince\Downloads\chromedriver_win32/chromedriver.exe')
browser.get('https://www.instagram.com/ajaydevgn/?hl=en')
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Parse HTML source page: Open the source page and use beautiful soup to parse it. Go through the body of html script and extract link for each image in that page and pass it to an empty list ‘links[]’
links=[]
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
page_json = script.text.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)
#try 'script.string' instead of script.text if you get error on index out of range
for link in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
    links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')
#try with ['display_url'] instead of ['shortcode'] if you don't get links 



#Extract links from hashtag page
links=[]
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
page_json = script.text.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)
for link in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
    links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')
    
#Get details for each post
#Go through every link in the list and extract detailed information to a pandas dataframe



result=pd.DataFrame()


import os
import requests
result.index = range(len(result.index))
directory="/directory/you/want/to/save/images/"
for i in range(len(result)):
    r = requests.get(result['display_url'][i])
    with open(directory+result['shortcode'][i]+".jpg", 'wb') as f:
                    f.write(r.content)
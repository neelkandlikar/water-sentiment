#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
import math
import time
from tqdm import tqdm
import os
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import xmltodict as saveme


#pip install xmltodict

wkdir = os.path.dirname(os.getcwd())

data_dir  = wkdir + '/data'

search_results = pd.read_csv(data_dir+'/scopus_search_results.csv', low_memory = False)

search_results['date'] = pd.to_datetime(search_results['prism:coverDate'], format='%Y-%m-%d', errors='coerce')

search_results = search_results[search_results.date.notna()]

api_key = open(wkdir+'/code/keys.gitignore', "r").readlines()

print('Master dataframe of search results imported')


print('Beginning of song to retrieve abstracts:')

#make an empty list to store failures
failed_pages = pd.DataFrame()

# create master dataframe with all the first article in the list

idx = search_results.iloc[0]['dc:identifier'].split(':')[1]
response = requests.get('https://api.elsevier.com/content/abstract/scopus_id/'+idx+'?view=META_ABS&apikey='+ api_key[2])

abstracts = pd.json_normalize(saveme.parse(response.text))


for i, a in tqdm(search_results[1:].iterrows()):
    try:
        #print("Working on article " + str(i) +' of'  + str(len(search_results)))
        #Get scupis ID:
        idx = a['dc:identifier'].split(':')[1]

        #Format URL to retrieve the abstract:
        response = requests.get('https://api.elsevier.com/content/abstract/scopus_id/'+idx+'?view=META_ABS&apikey='+ api_key[2])
        abstract = pd.json_normalize(saveme.parse(response.text))
        abstracts = abstracts.append(abstract)
    except:
        failed_pages[i] = idx
        continue
    time.sleep(0.12)
    
abstracts.to_csv(wkdir+'/data/abstracts_full.csv')
failed_pages.to_csv(wkdir+'/data/failed_queries.csv')

print('Failed abstract retrievals (' + str(len(failed_pages))+') saved to '+ data_dir)

print("Ding, end of song!")


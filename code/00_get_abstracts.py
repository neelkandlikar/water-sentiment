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
from tqdm import tqdm
import timeit
#pip install xmltodict

# Get the working and data directory paths
wkdir = os.path.dirname(os.getcwd())
data_dir  = wkdir + '/data'

#Load in the SCOPUS WOS Search Results
search_results = pd.read_csv(data_dir+'/scopus_search_results_r4.csv', low_memory = False)

# !! Import list of API Keys
api_keys = open(wkdir+'/code/keys.gitignore', "r").read().splitlines()


print('Master dataframe of search results imported with '+str(len(search_results['eid'].unique()))+' unique entries.')

#split list into 19 chunks:

chunks = range(8713, int(8e4)+8713, 2)

print('Beginning of song to retrieve abstracts:')

for i, chunk in enumerate(chunks):
    print('Retrieving abstracts ' +str(i)+ ' to ' +str(str(i+int(1e4))))
    #set the api_key for this chunk
    api_key = api_keys[i]
    
    #make an empty list to store failures
    failed_pages = pd.DataFrame()

    # create master dataframe with all the first article in the list

    idx = search_results.iloc[chunk]['dc:identifier'].split(':')[1]
    response = requests.get('https://api.elsevier.com/content/abstract/scopus_id/'+idx+'?view=META_ABS&apikey='+ api_key)

    abstracts = pd.json_normalize(saveme.parse(response.text))

    for j, a in tqdm(search_results[chunk+1:chunk+int(1e4)].iterrows(), desc='Chunk '+str(i)):
        try:
            #print("Working on article " + str(i) +' of'  + str(len(search_results)))
            #Get scupis ID:
            idx = a['dc:identifier'].split(':')[1]

            #Format URL to retrieve the abstract:
            response = requests.get('https://api.elsevier.com/content/abstract/scopus_id/'+idx+'?view=META_ABS&apikey='+ api_key)
            abstract = pd.json_normalize(saveme.parse(response.text))
            abstracts = abstracts.append(abstract)
            
            time.sleep(0.12)
            
        except:
            failed_pages[j] = idx
            continue
            
    abstracts.to_csv(wkdir+'/data/abstracts_chunk_'+str(i+1)+'.csv')
    
    if len(failed_pages) > 0:
        failed_pages.to_csv(wkdir+'/data/failed_queries_chunk'+str(i+1)+'.csv')
        print('Failed abstract retrievals (' + str(len(failed_pages))+') saved to '+ data_dir)
    else:
        print('Zero failed retrievals.')
        continue
    
    time.sleep(0.12)
        
    print('Done with chunk '+str(i))

print("Ding, end of song!")
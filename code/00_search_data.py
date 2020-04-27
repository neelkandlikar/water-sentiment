#!/usr/bin/env python
# coding: utf-8

# In[64]:


import pandas as pd
import requests
import math
import time
from tqdm import tqdm
import os


# In[2]:


api_key = open("/Users/corey/Documents/GitHub/WaterSentiment/code/keys.gitignore", "r").readlines()
api_key[2]


# In[4]:


#gathering info about the database, and how we'll need to query it
response0 = requests.get('https://api.elsevier.com/content/search/index:SCOPUS?query=ABS('+terms+')&apikey='+ api_key[2])
num_results = int(response0.json()['search-results']['opensearch:totalResults'])

entries = response0.json()['search-results']['entry']
entries_per = len(entries)
print ('Number of entries per response: ', entries_per, '\nTotal entries in database: ', num_results) #, \
       #f'\n{entries_per}-entry pages to get:', str(num_results//50), f'\nplus last page with {num_results%entries_per} entries')


# ### Run the search to return successive results, after resting, and build a list of SCOPUS article IDs
# 
# 
# 

# In[ ]:


###
terms = '"ground water" OR groundwater OR ground-water OR aquifer'

# Make a list of years to iterate over
yrs = range(1920, 2021, 1)

#make an empty list to store failures
failed_pages = []

#creat a pandas dataframe with the entries from the first page above:

for y in [yrs]:
    #Get the number of results per year
    response0 = requests.get('https://api.elsevier.com/content/search/index:SCOPUS?query=ABS('+terms+')&date='+str(y)+'&apikey='+ api_key[2])
    
    num_results = int(response0.json()['search-results']['opensearch:totalResults'])
    print('Number of journal articles for '+ str(y) + ':'+ str(num_results))
    
    #Create a list of page results
    if num_results > 25:
        chunks = range(0, int(num_results/25)+1, 1)
    else:
        chunks = [0]
    
    #create a data frame with the first result
    results = response0.json()['search-results']['entry']
    j = pd.json_normalize(results[0])

    #search the API, starting at each point where you left off, and pausing each iteration
    for chunk in tqdm(chunks):
        try:
            response = requests.get('https://api.elsevier.com/content/search/index:SCOPUS?query=ABS('+terms+')&date='+str(y) + '&start='+str(chunk)+ '&apikey='+api_key[2])
            for i, entry in enumerate(response.json()['search-results']['entry']):
                j = j.append(pd.json_normalize(entry))
        except:
            failed_pages.append([y, chunk]) 
            print('failed at page ' + str(chunk)+ ' for year ' +str(y))
            continue
            #break
        time.sleep(0.12)
    j.to_csv('/Users/corey/Documents/GitHub/WaterSentiment/data/annual_csvs/scopus_search_year'+str(y)+'.csv')
    print('Done with year '+str(y))


# In[59]:


## Combine the annual search results into one dataframe and case as csv to data folder


# get working directory

wkdir = os.path.dirname(os.getcwd())

csvs_dir  = wkdir + '/data/annual_csvs'

file_paths = []

for (dirpath, dirnames, filenames) in os.walk(csvs_dir):
    for f in filenames:
        file_paths.append(os.path.join(csvs_dir, f))
        
        
#Create amster dataframe

master_df = pd.read_csv(file_paths[0])

#Loop through and append each dataframe to the master from the diorectory of annual csvs

for y in file_paths:
    master_df = master_df.append(pd.read_csv(y))

master_df.to_csv(wkdir + '/data/scopus_search_results.csv')


#!/usr/bin/env python
# coding: utf-8

# In[370]:


import pandas as pd
import requests
import math
import time
from tqdm import tqdm
import os
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import xmltodict as saveme
from tqdm import tqdm_notebook


# In[ ]:


#pip install xmltodict


# In[368]:


wkdir = os.path.dirname(os.getcwd())

data_dir  = wkdir + '/data'

search_results = pd.read_csv(data_dir+'/scopus_search_results.csv', low_memory = False)

search_results['date'] = pd.to_datetime(search_results['prism:coverDate'], format='%Y-%m-%d', errors='coerce')

search_results = search_results[search_results.date.notna()]
# search_results = search_results.set_index('date')

api_key = open("/Users/corey/Documents/GitHub/WaterSentiment/code/keys.gitignore", "r").readlines()

print('Master dataframe of search results imported')


# In[383]:


print('Beginning of song to retrieve abstracts:')

#make an empty list to store failures
failed_pages = []

# create master dataframe with all the first article in the list

idx = search_results.iloc[0]['dc:identifier'].split(':')[1]
response = requests.get('https://api.elsevier.com/content/abstract/scopus_id/'+idx+'?view=META&apikey='+ api_key[2])

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
        failed_pages = failed_pages.append(idx)
        continue
    time.sleep(0.12)
    
abstracts.to_csv(wkdir+'/data/abstracts_full.csv')

print('Failed abstract retrievals: ' + str(len(failed_pages)), "\n", failed_pages)

print("Ding, end of song!")


# In[382]:


idx


# In[297]:



# dates = []
# cals = []

# for t in search_results.iterrows():
#     try:
#         #print(t)
#         dates.append(t[0])
#         title = t[1][7]
#         cals.append("california" in title.lower())
#     except:
#         continue


# In[303]:


# cali = pd.DataFrame({'dates': dates, 'calis': cals})
# cali = cali.set_index('dates')

# cali.sum()


# In[330]:


# grps = pd.DataFrame(search_results.eid.groupby(search_results.index.year).count())

# grps['calis'] = yrs['calis']

# ax = grps.plot(x=grps.index, kind='bar')

# # Make most of the ticklabels empty so the labels don't get too crowded
# ticklabels = ['']*len(search_results.index)
# # Every 4th ticklable shows the month and day
# #ticklabels[::4] = [item.strftime('%b %d') for item in search_results.index[::4]]
# # Every 12th ticklabel includes the year
# ticklabels[::12] = [item.strftime('%b %d\n%Y') for item in search_results.index[::12]]
# ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
# ax.set_ylabel('article count')
# ax.set_title('"ground water" OR groundwater OR ground-water OR aquifer')
# plt.tight_layout()
# plt.savefig('article_counts.png', dpi=300)


# In[ ]:





# In[ ]:





# In[ ]:





{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 64,
   "metadata": {
    "colab": {},
    "colab_type": "code",
    "id": "lkwInhSkZ5uQ"
   },
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import requests\n",
    "import math\n",
    "import time\n",
    "from tqdm import tqdm\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "colab": {},
    "colab_type": "code",
    "id": "vcHNz1DGbxis"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'19ab7c717adf69e87207438e0624dade'"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "api_key = open(\"/Users/corey/Documents/GitHub/WaterSentiment/code/keys.gitignore\", \"r\").readlines()\n",
    "api_key[2]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 86
    },
    "colab_type": "code",
    "id": "yZOnEFILI5Cs",
    "outputId": "378a6410-2367-452d-e0e2-f4c273b200f9"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Number of entries per response:  25 \n",
      "Total entries in database:  183826 \n",
      "25-entry pages to get: 3676 \n",
      "plus last page with 1 entries\n"
     ]
    }
   ],
   "source": [
    "#gathering info about the database, and how we'll need to query it\n",
    "response0 = requests.get('https://api.elsevier.com/content/search/index:SCOPUS?query=ABS('+terms+')&apikey='+ api_key[2])\n",
    "num_results = int(response0.json()['search-results']['opensearch:totalResults'])\n",
    "\n",
    "entries = response0.json()['search-results']['entry']\n",
    "entries_per = len(entries)\n",
    "print ('Number of entries per response: ', entries_per, '\\nTotal entries in database: ', num_results) #, \\\n",
    "       #f'\\n{entries_per}-entry pages to get:', str(num_results//50), f'\\nplus last page with {num_results%entries_per} entries')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "0WodwZsojIK5"
   },
   "source": [
    "### Run the search to return successive results, after resting, and build a list of SCOPUS article IDs\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "###\n",
    "terms = '\"ground water\" OR groundwater OR ground-water OR aquifer'\n",
    "\n",
    "# Make a list of years to iterate over\n",
    "yrs = range(1920, 2021, 1)\n",
    "\n",
    "#make an empty list to store failures\n",
    "failed_pages = []\n",
    "\n",
    "#creat a pandas dataframe with the entries from the first page above:\n",
    "\n",
    "for y in [yrs]:\n",
    "    #Get the number of results per year\n",
    "    response0 = requests.get('https://api.elsevier.com/content/search/index:SCOPUS?query=ABS('+terms+')&date='+str(y)+'&apikey='+ api_key[2])\n",
    "    \n",
    "    num_results = int(response0.json()['search-results']['opensearch:totalResults'])\n",
    "    print('Number of journal articles for '+ str(y) + ':'+ str(num_results))\n",
    "    \n",
    "    #Create a list of page results\n",
    "    if num_results > 25:\n",
    "        chunks = range(0, int(num_results/25)+1, 1)\n",
    "    else:\n",
    "        chunks = [0]\n",
    "    \n",
    "    #create a data frame with the first result\n",
    "    results = response0.json()['search-results']['entry']\n",
    "    j = pd.json_normalize(results[0])\n",
    "\n",
    "    #search the API, starting at each point where you left off, and pausing each iteration\n",
    "    for chunk in tqdm(chunks):\n",
    "        try:\n",
    "            response = requests.get('https://api.elsevier.com/content/search/index:SCOPUS?query=ABS('+terms+')&date='+str(y) + '&start='+str(chunk)+ '&apikey='+api_key[2])\n",
    "            for i, entry in enumerate(response.json()['search-results']['entry']):\n",
    "                j = j.append(pd.json_normalize(entry))\n",
    "        except:\n",
    "            failed_pages.append([y, chunk]) \n",
    "            print('failed at page ' + str(chunk)+ ' for year ' +str(y))\n",
    "            continue\n",
    "            #break\n",
    "        time.sleep(0.12)\n",
    "    j.to_csv('/Users/corey/Documents/GitHub/WaterSentiment/data/annual_csvs/scopus_search_year'+str(y)+'.csv')\n",
    "    print('Done with year '+str(y))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "metadata": {},
   "outputs": [],
   "source": [
    "## Combine the annual search results into one dataframe and case as csv to data folder\n",
    "\n",
    "\n",
    "# get working directory\n",
    "\n",
    "wkdir = os.path.dirname(os.getcwd())\n",
    "\n",
    "csvs_dir  = wkdir + '/data/annual_csvs'\n",
    "\n",
    "file_paths = []\n",
    "\n",
    "for (dirpath, dirnames, filenames) in os.walk(csvs_dir):\n",
    "    for f in filenames:\n",
    "        file_paths.append(os.path.join(csvs_dir, f))\n",
    "        \n",
    "        \n",
    "#Create amster dataframe\n",
    "\n",
    "master_df = pd.read_csv(file_paths[0])\n",
    "\n",
    "#Loop through and append each dataframe to the master from the diorectory of annual csvs\n",
    "\n",
    "for y in file_paths:\n",
    "    master_df = master_df.append(pd.read_csv(y))\n",
    "\n",
    "master_df.to_csv(wkdir + '/data/scopus_search_results.csv')"
   ]
  }
 ],
 "metadata": {
  "colab": {
   "collapsed_sections": [],
   "name": "00_search_data",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

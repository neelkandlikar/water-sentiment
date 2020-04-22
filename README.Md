# WaterSentiment

Collab between

* Kyra Kim (JPL)
* Corey Scher (CUNY)
* Rich Pauloo (UC Davis)
* Aakash Ahamed (SU)

# Abstract

Groundwater is critical to global food systems and drinking water. Groundwater is also hard to study: hidden beneath our feet in complex underground aquifers. This makes scientific accounting of groundwater inventories exceptionally difficult at the global scale. We propose a meta-study of global groundwater research to assemble the first global picture of geographic trends in groundwater research. The work will employ and mentor an undergraduate in need, who lost work due to COVID-19.

# Summary

This bibliometrics study will draw on established approaches for handling large corpora, drawing from text mining, natural language processing, and Latent Dirichlet Allocation (LDA) topic models in order to analyze sentiment trends in groundwater-specific scientific literature over time.

First, a corpus of relevant groundwater literature will be mined by searching for groundwater related keywords (e.g., “groundwater”, “aquifer”, “hydrogeology”) in article abstract text using the Web of Science API. Once literature has been identified, we will characterize the sentiment of each paper’s abstract using three approaches of increasing complexity and accuracy: (1) classical sentiment analysis approaches based on “bag of words” techniques, (2) a pre-trained neural network BERT models for more advanced, context-sensitive sentiment analysis, and (3) a pre-trained neural network called SciBERT, specifically designed for pattern recognition in scientific manuscripts. If the manuscript includes a study site, we will determine the location(s) for that study with similar pattern-matching techniques. 

This information will allow us to address our key question whether the sentiment of groundwater studies has changed over time, coincident with global groundwater resource depletion, and how trends vary over time and across regions worldwide.
Sentiment analysis via “bag of words” techniques works by categorizing words as either positive, negative, or neutral in connotation, enabling us to track the evolving state of  groundwater science at key aquifers around the world. For example, frequent use of negative words such as “scarcity”, “depletion”, and “competition” would indicate groundwater resources in a certain region are being contentiously sought after. In  contrast, increased frequency of positive words such as “collaboration”, “stable”, and “sustainable” would highlight the progress in groundwater sustainability. However, these simple “bag of words” methods may miss context dependent sentiments. For example, “in Country A’s aquifer, we observed a reversal of groundwater depletion trends over time, evidenced by increasing groundwater levels” contains the word “depletion” but has a positive connotation. A pre-trained classifier like BERT or SciBERT may be able to resolve these nuances in context-dependent meaning. Moreover, we will manually verify that these methods work as intended, and make corrections as necessary.

In order to understand the range of topics studied in the literature, we will fit LDA topic models to the corpus, and investigate the resulting clusters for prevailing themes in the literature. Next, we will segment the literature into 10-year-long bins in order to analyze decadal changes in topics, and relate these back to the sentiment scores over time and location.
The distribution of global groundwater resources is well studied, but the distribution of global groundwater research remains unknown. We will compare the research discovered to these known locations, with an eye towards disparities in research abundance, and discuss these trends in terms of the hydrogeologic, climatic, and water management characteristics on a per-region basis.


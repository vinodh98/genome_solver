import requests
import re
from bs4 import BeautifulSoup
from bs4 import Comment

# Initialize query paprameters
# Check the parameter list at https://ncbi.github.io/blast-cloud/dev/api.html
Protein = 'YP_009160396.1'

###############
# STEP 3
###############
# get the page results
# 
# https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID=UCRP4DU9014

# debug
rid='UCPEJJM5015'
Web_Site ='https://blast.ncbi.nlm.nih.gov/Blast.cgi?'
Web_Data = 'CMD=Get&RID='+rid
query = Web_Site+Web_Data
print(query)
# Submit the request to the BLAST site
page = page_request.content

#https://blast.ncbi.nlm.nih.gov/Blast.cgi?QUERY=YP_009160396.1&DATABASE=nr&PROGRAM=blastp&FORMAT_EQ_MENU=txid2 [ORGN]&CMD=Put&FORMAT_TYPE=XML
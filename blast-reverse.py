import requests
import re
from bs4 import BeautifulSoup
from bs4 import Comment

# Initialize query paprameters
# Check the parameter list at https://ncbi.github.io/blast-cloud/dev/api.html
Protein = 'OSJ99870.1'
Domain = 'ENTREZ_QUERY=txid10239[ORGN]'
###############
# STEP 1
###############
# build the request to query / blast
Web_Site ='https://blast.ncbi.nlm.nih.gov/Blast.cgi?'
Web_Data = 'QUERY='+Protein+'&DATABASE=nr&PROGRAM=blastp&'+Domain+'&CMD=Put&FORMAT_TYPE=XML'
query = Web_Site+Web_Data
print(query)

# Submit the request to the BLAST site
page_request = requests.put(query)
page = page_request.content
print(page)
#https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&VIEW_RESULTS=FromRes&RID=U51ER5YC014&UNIQ_OBJ_NAME=A_SearchResults_1iJTDs_G8z_dgudRZRI7eV_GTXQl_9VYno&QUERY_INDEX=0

# save the page for troubleshooting
f = open("query-submit.html", "wb")
f.write(page)
f.close()


# Load the request response content to BeautifulSoup
soup = BeautifulSoup(page,"html.parser")

comments = soup.find_all(string=lambda text: isinstance(text, Comment))
for eachcomment in comments:
    if 'QBlastInfoBegin' in str(eachcomment):
        #print(eachcomment)
        #getids=re.findall(r"RID = \w+",eachcomment)
        getids=re.findall("= \w+",eachcomment)
        rid=re.sub("= ", "", getids[0])
        rtoe=re.sub("= ", "", getids[1])
        #print("RID =",rid,"\nRTOE=",rtoe)
        print(rid)
        print(rtoe)
###############
# STEP 2
###############
# Check the status of the submitted query
#

#QBlastInfoBegin
#    Status=READY
#QBlastInfoEnd
#QBlastInfoBegin
#	ThereAreHits=yes
#QBlastInfoEnd

#CMD=Get, FORMAT_OBJECT=SearchInfo, and RID=VALUE
# https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=UCYAZVZY01R
Web_Data = 'CMD=Get&FORMAT_OBJECT=SearchInfo&RID='+rid
query = Web_Site+Web_Data
print(query)
# Submit the request to the BLAST site
page_request = requests.put(query)
page = page_request.content

# save the page for troubleshooting
f = open("query-status.html", "wb")
f.write(page)
f.close()
soup = BeautifulSoup(page,"html.parser")

comments = soup.find_all(string=lambda text: isinstance(text, Comment))
for eachcomment in comments:
    if 'Status=READY' in str(eachcomment):
        print(eachcomment)
        getstatus=re.findall("=\w+",eachcomment)
        status=re.sub("=", "", getstatus[0])

###############
# STEP 3
###############
# get the page results
#
# https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID=VHM92P8Z01R

# debug
#rid="UCH5A3NU015"
Web_Site ='https://blast.ncbi.nlm.nih.gov/Blast.cgi?'
Web_Data = 'CMD=Get&RID='+rid
query = Web_Site+Web_Data
print(query)
# Submit the request to the BLAST site
page_request = requests.put(query)
page = page_request.content
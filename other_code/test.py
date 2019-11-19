# Step 1
# Submit the protein query to the queue

#import urllib.request as ul
import requests
from html.parser import HTMLParser

# ------- Auxilary Routines and Classes -----------------

# A simple routine that extracts an Attribute from a Context given the surrounding marking strings

def ExtractAttribute(Context, Attribute, Start_Mark, End_Mark):
    Attribute_Position = Context.find(Attribute)
    if Attribute_Position>=0:
        Mark_Position = Context.find(Start_Mark)+len(Start_Mark)
        Attribute_Value = (Context[Mark_Position:Context.find(End_Mark,Mark_Position)]).strip(" ")
        return Attribute_Value

# Creating a subclass of HTMLParser and overriding the comment handler method

# We need to find a comment that contains "QBlastInfoBegin"
# Once the comment is found we need to extract from it the RID
# the RID line has the following format 'RID = "XXXXXXXXXXX"'
# the value in the RID line starts with "=" and ends with "\n"

class MyHTMLParser(HTMLParser):

    Tokens = []
    
    def handle_comment(self, data):
        if data.find('QBlastInfoBegin')>=0:
            self.Tokens.append(ExtractAttribute(data, "RID", "=", "\n"))

# ------- End Auxilary Routines and Classes -----------------
        
# Initialize query paprameters
# Check the parameter list at https://ncbi.github.io/blast-cloud/dev/api.html
Protein = 'YP_009160396.1'
Domain = 'FORMAT_EQ_MENU=txid2 [ORGN]' 

# Submit the request to the BLAST site
# Note that the Domain restriction can be added later, at the results retieval step
Web_Site ='https://blast.ncbi.nlm.nih.gov/Blast.cgi?'
Web_Data = 'QUERY='+Protein+'&DATABASE=nr&PROGRAM=blastp&'+Domain+'&CMD=Put&FORMAT_TYPE=TEXT'

# print(Web_Site+Web_Data)

query = Web_Site+Web_Data

#with ul.urlopen(query) as response:
# with urllib.request.post(Web_Request) as response:
#    page = response.read()

resp = requests.put(query)
# page = resp.content
page = resp.text

# page = ul.urlopen('https://blast.ncbi.nlm.nih.gov/Blast.cgi?QUERY='+Protein+'&DATABASE=nr&PROGRAM=blastp&'+Domain+'&CMD=Put&FORMAT_TYPE=TEXT').read()

parser = MyHTMLParser()
parser.feed(page)

# Save the return page for the future use
with open("Queue.html","w") as Queue_file:
    Queue_file.write(page)
    Queue_file.close

# If any RIDs were received record the first one in a file
if len(parser.Tokens)> 0:
    with open("RID.txt","w") as RID_file:
        RID_file.write(parser.Tokens[0])
        RID_file.close
#       print "First RID: ", parser.Tokens[0]
    
# print "Extracted RIDs: ", parser.Tokens

# When  you request with "GET" the executed query comes back.
# page = ul.urlopen('https://blast.ncbi.nlm.nih.gov/Blast.cgi?RID=TGVN71MB015&CMD=GET&FORMAT_TYPE=TEXT').read()

# This needs a unique Id
# page = ul.urlopen('https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=GetSaved&RECENT_RESULTS=on').read()

# What is remaining:
# Save two responses to a separate files not to disturb the server with each iteration
# Insert "TAXID" in the query
# Done: Retrieve "RID" from the first response
# Save RID to a separate file if the studies need to be restarted later
# Insert "RID" in the second query
# Wait until the second query is completed
# Extract the list of the proteins from the second queries
# Insert proteins from the second response into the third queries
# Retrieve "RID"s from all the third queries
# Issue forth queries with new retrieved "RIDs"
# Extract the list of the proteins from all the fourth queries

# print page
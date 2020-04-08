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

# Step 2
# Using existing study ids (RIDs) request the study results

# import a  module to handle Internet navigation requests
import urllib as ul


# Read the stored Query Id (RID) 
with open("RID.txt","r") as RID_file:
    RID = RID_file.read()
    RID_file.close

# Request the results of the study given the RID    
# Check parameters descriptors at  https://ncbi.github.io/blast-cloud/dev/api.html

Domain = 'FORMAT_EQ_MENU=txid2 [ORGN]' 
if len(RID)>0:
    # page = ul.urlopen('https://blast.ncbi.nlm.nih.gov/Blast.cgi?RID=' +RID+'&CMD=GET&FORMAT_TYPE=XML').read()
    # Note that the domain restriciton 'FORMAT_EQ_MENU=txid2 [ORGN]' should be included even if it was included in the original query 
    page = ul.urlopen('https://blast.ncbi.nlm.nih.gov/Blast.cgi?RID=' +RID+'&' + Domain + '&CMD=GET&FORMAT_TYPE=XML').read()

# Write the results of the study in the report file
    File_Name = "REP_" + RID + ".XML"
    with open(File_Name,"w") as Proteins_file:
        Proteins_file.write(page)
        Proteins_file.close

# Write the results of the study in the generic file
# This is not very elegant, but the XML file for the intitial protein is used in two ways: to start the search for homologs and to extract valid pairs: copying is a simple way to solve both purposes
    File_Name = "Proteins.XML"
    with open(File_Name,"w") as Proteins_file:
        Proteins_file.write(page)
        Proteins_file.close


# Step 3
# Extract protein pairs from the resulsts file using XML parser

# import a  module to handle xml file parsing
import xml.etree.ElementTree as ET

tree = ET.parse("Proteins.XML")
root = tree.getroot()

# Write the results of the study in the report file 

source = root.find('BlastOutput_query-ID').text

# Can use this naming scheme later
# File_Name = "HOMOLOG_"+source+".txt"

File_Name = "Homologs.txt"

with open(File_Name,"w") as Homolog_file:

    for hits in root.iter('Hit'):
        ahit = hits.find('Hit_accession').text
        Homolog_file.write(ahit+'\n')
    Homolog_file.close


# Step 4
# Submit studies from a list of homologs

import urllib as ul
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
Max_Studies = 3
Current_Study = 0
Domain = 'FORMAT_EQ_MENU=txid2 [ORGN]'
parser = MyHTMLParser()

# Read all the homologs to study
with open("Homologs.txt","r") as Homologs_File:
    Homologs = Homologs_File.readlines()
    Homologs_File.close

# Record study RIDs in an RID file
with open("HOMOLOG_RIDS.txt","w") as RIDs_File:
    # For each protein in Homologs initiated a study but no more than max number of studies
    for Entry in Homologs:
        Current_Study +=1
        if Current_Study <= Max_Studies: 
            Protein = Entry.replace("\n", "")
            # Request a RID for each Homolog
            page = ul.urlopen('https://blast.ncbi.nlm.nih.gov/Blast.cgi?QUERY='+Protein+'&DATABASE=nr&PROGRAM=blastp&'+Domain+'&CMD=Put&FORMAT_TYPE=TEXT').read()
            parser.feed(page)
            if len(parser.Tokens)> 0:
                RIDs_File.write(parser.Tokens[-1]+"\n")
    RIDs_File.close


# Step 5
# Using Homolog RIDs request the study results

# import a  module to handle Internet navigation requests
import urllib as ul


Domain = 'FORMAT_EQ_MENU=txid2 [ORGN]' 

# Read the stored Query Id (RID) 
with open("Homolog_RIDs.txt","r") as RID_file:
    RID_list = RID_file.readlines()
    RID_file.close

for entry in RID_list:
    RID = entry.replace("\n","")


    # Request the results of the study given the RID    
    # Check parameters descriptors at  https://ncbi.github.io/blast-cloud/dev/api.html

    if len(RID)>0:
        # page = ul.urlopen('https://blast.ncbi.nlm.nih.gov/Blast.cgi?RID=' +RID+'&CMD=GET&FORMAT_TYPE=XML').read()
        # Note that the domain restriciton 'FORMAT_EQ_MENU=txid2 [ORGN]' should be included even if it was included in the original query 
        page = ul.urlopen('https://blast.ncbi.nlm.nih.gov/Blast.cgi?RID=' +RID+'&' + Domain + '&CMD=GET&FORMAT_TYPE=XML').read()

        # Write the results of the study in the report file

        File_Name = "REP_" + RID + ".XML"
        with open(File_Name,"w") as Proteins_file:
            Proteins_file.write(page)
            Proteins_file.close

# Step 6
# Extract protein pairs from all the Report Files in the directory

# import a  module to handle xml file parsing
import xml.etree.ElementTree as ET
import glob

# Select all report files
Pairs_Report = "All Pairs.txt"
Report_Files = []

for file in glob.glob("REP_*.xml"):
    Report_Files.append(file)

with open(Pairs_Report,"w") as Pairs_File:
    for File_Name in Report_Files:
        tree = ET.parse(File_Name)
        root = tree.getroot()

        # Write the results of the study in the report file 

        source = root.find('BlastOutput_query-ID').text

        for hits in root.iter('Hit'):
            ahit = hits.find('Hit_accession').text
            Pairs_File.write(source+"___ "+ahit+'\n')
    Pairs_File.close





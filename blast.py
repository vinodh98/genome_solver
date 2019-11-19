import requests
import re
import time

# ------- Auxiliary Routines and Classes -----------------
# A simple routine that extracts an Attribute from a Context given the surrounding marking strings
def extract_attribute(data, attribute):
    print("Looking for the attribute:", attribute)
    for line in data.splitlines():
        if attribute in line:
            print(line)
            attribute_value = re.sub(attribute, "", line)
            attribute_value = re.sub(r"\s", "", attribute_value)
            return attribute_value


# ------- End Auxiliary Routines and Classes -----------------

###############
# STEP 1
###############
# Initialize query parameters
# Check the parameter list at https://ncbi.github.io/blast-cloud/dev/api.html
Protein = 'YP_009160396.1'
Domain_Filter = 'ENTREZ_QUERY=txid2[ORGN]'  # Bacteria
# build the URL Submit request
URL_Endpoint = 'https://blast.ncbi.nlm.nih.gov/Blast.cgi?'
URL_Request = 'QUERY=' + Protein + '&DATABASE=nr&PROGRAM=blastp&' + Domain_Filter + '&CMD=Put'
URL_Submit = URL_Endpoint + URL_Request
print(URL_Submit)

# Submit the request to the BLAST site
Submit_Request = requests.put(URL_Submit)

# Save the Submit result for troubleshooting
f = open("query-submit.html", "w")
f.write(Submit_Request.text)
f.close()

rid = extract_attribute(Submit_Request.text, "RID = ")
print(rid)
rtoe = extract_attribute(Submit_Request.text, "RTOE = ")
print(rtoe)

###############
# STEP 2
###############
# https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=W8BRVRZW014

Wait_for_blast_completion = int(rtoe)*60
print("Ok going to sleep for ", Wait_for_blast_completion, " seconds or ", rtoe, "minutes")
time.sleep(Wait_for_blast_completion)
print("Ok I'm up, ready to check if the search is complete")

URL_Request = 'CMD=Get&FORMAT_OBJECT=SearchInfo&RID='+rid
URL_Submit = URL_Endpoint + URL_Request

# Submit the request to the BLAST site
Submit_Request = requests.put(URL_Submit)

# Save the Submit result for troubleshooting
f = open("query-status.html", "w")
f.write(Submit_Request.text)
f.close()

query_status = extract_attribute(Submit_Request.text, "Status=")
print(query_status)
query_hits = extract_attribute(Submit_Request.text, "ThereAreHits=")
print(query_hits)

if query_status == 'READY' and query_hits == 'yes':
    print("We got some hits yay ! ok will grab the JSON file")
    # https://blast.ncbi.nlm.nih.gov/Blast.cgi?RESULTS_FILE=on&FORMAT_TYPE=JSON2_S&FORMAT_OBJECT=Alignment&CMD=Get&RID=W3NDU16Z015
    URL_Request = 'RESULTS_FILE=on&FORMAT_TYPE=JSON2_S&FORMAT_OBJECT=Alignment&CMD=Get&RID=' + rid
    Submit_JSONRequest = requests.put(URL_Endpoint+URL_Submit)
    print(Submit_JSONRequest)

else:
    print("NCBI time projection is wrong! I give up:", URL_Submit)

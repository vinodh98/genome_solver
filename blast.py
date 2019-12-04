import requests
import re
import time

# Initialize query parameters
# Check the parameter list at https://ncbi.github.io/blast-cloud/dev/api.html
Protein = 'YP_009160396.1'
Domain_Filter = 'ENTREZ_QUERY=txid2[ORGN]'  # Bacteria
# build the URL Submit request
url_endpoint = 'https://blast.ncbi.nlm.nih.gov/Blast.cgi?'


# ------- Auxiliary Routines and Classes -----------------
# A simple routine that extracts an Attribute from a Context given the surrounding marking strings
def extract_attribute(data, attribute):
    # print("Looking for the attribute:", attribute)
    for line in data.splitlines():
        if attribute in line:
            print(line)
            attribute_value = re.sub(attribute, "", line)
            attribute_value = re.sub(r"\s", "", attribute_value)
            return attribute_value


# ------- End Auxiliary Routines and Classes -----------------

# ------- Auxiliary Routines and Classes -----------------
# A simple routine that checks the status of the given RID
def check_request_status(requestid):
    print("Checking status of RID:", requestid)
    url_request = 'CMD=Get&FORMAT_OBJECT=SearchInfo&RID=' + rid
    url_submit = url_endpoint + url_request
    # Submit the request to the BLAST site
    submit_request = requests.put(url_submit)

    # Save the Submit result for troubleshooting
    file_handle = open("query-status.html", "w")
    file_handle.write(submit_request.text)
    file_handle.close()

    query_status = extract_attribute(submit_request.text, "Status=")
    #print(query_status)
    query_hits = extract_attribute(submit_request.text, "ThereAreHits=")
    #print(query_hits)
    return query_status, query_hits


# ------- End Auxiliary Routines and Classes -----------------


###############
# STEP 1
###############

url_request = 'QUERY=' + Protein + '&DATABASE=nr&PROGRAM=blastp&' + Domain_Filter + '&CMD=Put'
url_submit = url_endpoint + url_request
print(url_submit)

# Submit the request to the BLAST site
Submit_Request = requests.put(url_submit)

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

while True:
    Status, Hits = check_request_status(rid)
    if Status == 'READY' and Hits == 'yes':
        print("We got some hits yay ! ok will grab the JSON file")
        break
    else:
        print("Will wait and try in 60 seconds")
        #print("Will wait for 60 seconds and try the url again - https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=",rid)
        time.sleep(60)

url_request = 'RESULTS_FILE=on&FORMAT_TYPE=JSON2_S&FORMAT_OBJECT=Alignment&CMD=Get&RID=' + rid
Submit_JSONRequest = requests.put(url_endpoint + url_submit)
#print(Submit_JSONRequest)

# Save the Submit result for troubleshooting
save_json_file_handle = open("results.json", "w")
save_json_file_handle.write(Submit_JSONRequest.text)
save_json_file_handle.close()

print("All Done")
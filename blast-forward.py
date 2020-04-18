import requests
import re
import time
import json

# Initialize query parameters
# Check the parameter list at https://ncbi.github.io/blast-cloud/dev/api.html
Protein = 'YP_009160396.1'
Domain_Filter = 'ENTREZ_QUERY=txid2[ORGN]'  # Limit to Bacteria
# build the URL Submit request
url_endpoint = 'https://blast.ncbi.nlm.nih.gov/Blast.cgi?'


# ## ------- Auxiliary Routines and Classes -----------------
# A simple routine that extracts an Attribute from a Context given the surrounding marking strings
# ##
def extract_attribute(data, attribute):
    # print("Looking for the attribute:", attribute)
    for line in data.splitlines():
        if attribute in line:
            print(line)
            attribute_value = re.sub(attribute, "", line)
            attribute_value = re.sub(r"\s", "", attribute_value)
            return attribute_value


# ## ------- End Auxiliary Routines and Classes -----------------

# ## ------- Auxiliary Routines and Classes -----------------
# A simple routine that checks the status of the given RID
# ##

def check_request_status(requestid):
    #print("Checking status of RID:", requestid)
    url_request = 'CMD=Get&FORMAT_OBJECT=SearchInfo&RID=' + rid
    url_submit = url_endpoint + url_request
    # Submit the request to the BLAST site
    submit_request = requests.put(url_submit)

    # Save the Submit result for troubleshooting
    file_handle = open("query-status.html", "w")
    file_handle.write(submit_request.text)
    file_handle.close()

    query_status = extract_attribute(submit_request.text, "Status=")
    # print(query_status)
    query_hits = extract_attribute(submit_request.text, "ThereAreHits=")
    # print(query_hits)
    return query_status, query_hits


# ## ------- End Auxiliary Routines and Classes -----------------


###############
# STEP 1
###############

url_request = 'QUERY=' + Protein + '&DATABASE=nr&PROGRAM=blastp&' + Domain_Filter + '&CMD=Put'
url_submit = url_endpoint + url_request

# Submit the request to the BLAST site
Submit_Request = requests.put(url_submit)

# Save the Submit result for troubleshooting
f = open("query-submit.html", "w")
f.write(Submit_Request.text)
f.close()

rid = extract_attribute(Submit_Request.text, "RID = ")
#print(rid)
rtoe = extract_attribute(Submit_Request.text, "RTOE = ")
#print(rtoe)

###############
# STEP 2
###############
# https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=3BZF6X4G016
print("Check the status via web-browser:")
print("https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID="+rid)
while True:
    Status, Hits = check_request_status(rid)
    if Status == 'READY' and Hits == 'yes':
        print("We got some hits yay ! ok will grab the hits file")
        break
    elif Status == 'READY' and Hits == 'no':
        print("There seems to be a problem, we have no hits")
        print("Check via: https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=", rid)
        break
    else:
        print("Will wait and try in 60 seconds")
        # print("Will wait for 60 seconds and try the url again -
        # https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=",rid)
        time.sleep(60)

###############
# STEP 3
###############

# Download the file
# JSON File *
# "https://blast.ncbi.nlm.nih.gov/Blast.cgi?RESULTS_FILE=on&FORMAT_TYPE=JSON2_S&FORMAT_OBJECT=Alignment&CMD=Get&RID=3BV6047Z014"
# TXT File
# https://blast.ncbi.nlm.nih.gov/Blast.cgi?RESULTS_FILE=on&RID=9HDFGPKV016&FORMAT_TYPE=Text&FORMAT_OBJECT=Alignment&DESCRIPTIONS=100&ALIGNMENTS=100&CMD=Get&DOWNLOAD_TEMPL=Results_All&ADV_VIEW=on
# CSV File
# https://blast.ncbi.nlm.nih.gov/Blast.cgi?RESULTS_FILE=on&FORMAT_TYPE=CSV&FORMAT_OBJECT=Alignment&DESCRIPTIONS=10&ALIGNMENT_VIEW=Tabular&CMD=Get&RID=3BV6047Z014
# print(Submit_JSONRequest)
url_request = 'RESULTS_FILE=on&FORMAT_TYPE=JSON2_S&FORMAT_OBJECT=Alignment&CMD=Get&RID=' + rid
csv_header_row = 'query_id,scientific_name,query_cover_per,evalue,per_identity,accession_id'
Submit_JSONRequest = requests.get(url_endpoint + url_request)
save_json_file_handle = open("tmp/results.json", "w")
save_json_file_handle.write(Submit_JSONRequest.text)
save_json_file_handle.close()

print("Downloaded the file")

##
# STEP 4
##
# Parse the json file and write the top 10 results

output_csv_file = open("tmp/results.csv", "w")
csv_header_row = 'query_id,scientific_name,query_cover_per,evalue,per_identity,accession_id\n'
output_csv_file.write(csv_header_row)

with open("tmp/results.json", "r") as read_file:
    data = json.load(read_file)

# Extract the query details
query_id = data['BlastOutput2'][0]['report']['results']['search']['query_id']
query_len = data['BlastOutput2'][0]['report']['results']['search']['query_len']

print("###################################################")
print("Query Cover %\tE_Value\tAccession Id\tSubject Name")
print("###################################################")

# We need only the top 10 hits
hit_count = 0
for hit in data['BlastOutput2'][0]['report']['results']['search']['hits']:
    # Extract the hits
    scientific_name = hit['description'][0]['sciname']
    accession_id = hit['description'][0]['accession']
    hsps_align_len = hit['hsps'][0]['align_len']
    hsps_identity = hit['hsps'][0]['identity']
    hsps_query_from = hit['hsps'][0]['query_from']
    hsps_query_to = hit['hsps'][0]['query_to']
    evalue = hit['hsps'][0]['evalue']

    # https://codereview.stackexchange.com/questions/39879/calculate-query-coverage-from-blast-output)
    query_cover_per = ((hsps_query_to - hsps_query_from) / query_len) * 100

    per_identity = (hsps_identity / hsps_align_len) * 100
    if (query_cover_per > 70) and (hit_count < 10):
        if hit_count == 0:
            topHit = accession_id
            topHit_scientific_name = scientific_name
        hit_count += 1
        print(round(query_cover_per, 2), evalue, accession_id, scientific_name, sep='\t')
        row = ','.join(
            (query_id, scientific_name, str(query_cover_per), str(evalue), str(per_identity), accession_id)) + '\n'
        output_csv_file.write(row)
print("###################################################")
print("##### TOP HIT = " + topHit, topHit_scientific_name)
print("###################################################")
output_csv_file.close()

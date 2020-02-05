import requests
import re
import time
import csv

# Initialize query parameters
# Check the parameter list at https://ncbi.github.io/blast-cloud/dev/api.html
Protein = 'WP_084828638.1'
Domain_Filter = 'ENTREZ_QUERY=txid2[ORGN]'  # Limit to Viruses
# build the URL Submit request
url_endpoint = 'https://blast.ncbi.nlm.nih.gov/Blast.cgi?'


# ------- Auxiliary Routines and Classes -----------------
# A simple routine that extracts an Attribute from a Context given the surrounding marking strings
#
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
#
#
def check_request_status(requestid):
    print("Checking status of RID:", requestid)
    url_request = 'CMD=Get&FORMAT_OBJECT=SearchInfo&RID=' + rid
    url_submit = url_endpoint + url_request
    # Submit the request to the BLAST site
    submit_request = requests.put(url_submit)

    # Save the Submit result for troubleshooting
    file_handle = open("query-status-reverse.html", "w")
    file_handle.write(submit_request.text)
    file_handle.close()

    query_status = extract_attribute(submit_request.text, "Status=")
    # print(query_status)
    query_hits = extract_attribute(submit_request.text, "ThereAreHits=")
    # print(query_hits)
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
f = open("query-submit-reverse.html", "w")
f.write(Submit_Request.text)
f.close()

rid = extract_attribute(Submit_Request.text, "RID = ")
print(rid)
rtoe = extract_attribute(Submit_Request.text, "RTOE = ")
print(rtoe)

###############
# STEP 2
###############
# https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=3BZF6X4G016

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

# Download the JSON or CSV File
# CSV File
# https://blast.ncbi.nlm.nih.gov/Blast.cgi?RESULTS_FILE=on&FORMAT_TYPE=CSV&FORMAT_OBJECT=Alignment&DESCRIPTIONS=10&ALIGNMENT_VIEW=Tabular&CMD=Get&RID=3BV6047Z014
# JSON File
# "https://blast.ncbi.nlm.nih.gov/Blast.cgi?RESULTS_FILE=on&FORMAT_TYPE=JSON2_S&FORMAT_OBJECT=Alignment&CMD=Get&RID=3BV6047Z014"
# print(Submit_JSONRequest)
# url_request = 'RESULTS_FILE=on&FORMAT_TYPE=JSON2_S&FORMAT_OBJECT=Alignment&CMD=Get&RID=' + rid
url_request = 'RESULTS_FILE=on&FORMAT_TYPE=CSV&FORMAT_OBJECT=Alignment&DESCRIPTIONS=10&ALIGNMENT_VIEW=Tabular&CMD=Get' \
              '&RID=' + rid

csv_header_row = 'query_id,subject_id,per_identity,alignment_length,mismatches,gap_opens,q_start,q_end,s._start,' \
                 's._end,evalue,bit_score,sequence\n'
Submit_JSONRequest = requests.get(url_endpoint + url_request)
# save_file_handle = open("results.json", "w")
save_file_handle = open("results-reverse.csv", "w")
save_file_handle.write(csv_header_row)
save_file_handle.write(Submit_JSONRequest.text)
save_file_handle.close()

print("Downloaded the file")

##
# STEP 4
##
# Parse the csv file and write the top 10 results

csv_file = open("results-reverse.csv", "r")
dict_reader = csv.DictReader(csv_file)
i = 0
print("########################################")
print("Percentage \tSubject ID\tE_Value")
print("########################################")
for row in dict_reader:
    if float(row['per_identity']) > 70:
        # Save the top hit
        if i == 1:
            print(row['per_identity'], "\t", row['subject_id'], "\t", row['evalue'], "\t*")
            i += 1
            topHit = row['subject_id']
        else:
            i += 1
            print(row['per_identity'], "\t", row['subject_id'], "\t", row['evalue'])
print("########################################")
print("The top hit = ", topHit)

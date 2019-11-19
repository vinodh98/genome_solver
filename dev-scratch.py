#!/usr/bin/python
import re
import time

filename = "query-status.html"

# time test
#Wait_for_blast_completion = 1 * 60
#print("Ok going to sleep for " + str(Wait_for_blast_completion) + " seconds")
#time.sleep(Wait_for_blast_completion)
#print("Ok I'm up, ready to check the status")

# ------- Auxiliary Routines and Classes -----------------
# A simple routine that extracts an Attribute from a Context given the surrounding marking strings
def extract_attribute(data, attribute):
    print("Looking for the attribute:", attribute)
    for line in data:
        # print(line)
        if attribute in line:
            print(line)
            attribute_value = re.sub(attribute, "", line)
            attribute_value = re.sub(r"\s", "", attribute_value)
            return attribute_value


# ------- End Auxiliary Routines and Classes -----------------

with open(filename) as f:
    content = f.read().splitlines()

query_status = extract_attribute(content, "Status=")
print(query_status)
query_hits = extract_attribute(content, "ThereAreHits=")
print(query_hits)

if query_status == 'READY' and query_hits == 'yes':
    print("We got some hits yay ! ok will grab the JSON file")
else:
    print("NCBI time projection is wrong! I give up:", URL_Submit)

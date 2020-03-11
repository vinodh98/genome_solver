# Needed columns
    Description	
    Query Cover > 70%
    &
    E value < e^-50
    Per. Ident
    Accession

# Forward blast the protein, limited to records that include only Bacteria (taxid:2)
    - take the top hit (Accession #)
    - save the top 10 (Accession #) to file
        use the above conditions to filter dwon
# Reverse blast the top hit, this time limited to records that include only Viruses (taxid:10239)
    - take the top hit (Accession #)
        Compare this value (Accession #) with the top hit in the forward blast
            If they match then flag it as a "match"
    - save the top 10 (Accession #) to file

# TODO
    - Create sub routines
        - for check status
        - for submit requst
        - Get the result
        - Parse the items
        - Save the top 10 items
        - Revers the top hit
        - loop 
    - Learn and use JSON / XML parser
# Example output
### Forward Blast AZA18259.1 (Limit to Bacteria)
| Percentage | Subject ID |E_Value|
|--|--|--|
100.000| AZA18259.1| 0.0|
94.540| WP_084828638.1*| 0.0|
91.379| WP_111679482.1| 0.0|
76.012| WP_155214194.1| 0.0|
75.434| WP_155214166.1| 0.0|
**The top hit = WP_084828638.1**

---------------------------------------
### Reverse Blast WP_084828638.1 (Limit to Viruses)
| Percentage | Subject ID |E_Value|
|--|--|--|
95.690|YP_001686804.1|0.0|
95.690|ARU14331.1|0.0|
95.115|NP_056680.1|0.0|
94.540|AZA24404.1|0.0|
95.402|ARU13760.1|0.0|
94.253|YP_003344853.1|0.0|
95.115|ARU14608.1|0.0|
94.253|AZF92090.1|0.0|
95.115|AYP29589.1|0.0|
94.253|AYP30036.1|0.0|
**The top hit =  YP_001686804.1**   
```
ENTREZ_QUERY=txid2[ORGN]
https://blast.ncbi.nlm.nih.gov/Blast.cgi?QUERY=YP_009160331.1&DATABASE=nr&PROGRAM=blastp&ENTREZ_QUERY=txid2[ORGN]&CMD=Put&FORMAT_TYPE=XML
https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=UCZEPSED014
https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID=UCZEPSED014
https://blast.ncbi.nlm.nih.gov/Blast.cgi?RESULTS_FILE=on&RID=UCZEPSED014&FORMAT_TYPE=JSON2_S&FORMAT_OBJECT=Alignment&CMD=Get
QBlastInfoBegin
    Status=READY
QBlastInfoEnd
--></p> 
<!--
QBlastInfoBegin
    ThereAreHits=yes
QBlastInfoEnd
```

# Class setup 
1. PC / MAC / Whatever - web browser with Jupiter NB
        - https://colab.research.google.com/notebooks/welcome.ipynb
        - crash course / bootstrap
2. All the requirement for python modules should be there in the Jupyter Env
        - Beautiful Soup
        - Requests
        - REGEX "re"
        - XML / JSON
3. Pull the code from git

# Old Notes

The program has 6 steps. NCBI request fullfillments take time. The wait times are variable and mostly unpredictable.  Only Steps 2 and 5 are dependent on the NCBI delays.

Step 1.
Submits a given protein for study. The study is added to the NCBI list. The processing might get some time.
Input
	The protein name is given in the code itself (can be easily modified)
Output
	Two files are produced:
	Queue.html - contains the confiramtion of the submission to the queue
	RID.txt - contains the study ID (RID) that can be used to retireve the study results later.

Step 2.
Retieves the results of the study for a given RID
Input
	The RID is retrieved from RID_TXT
Output 
	Two report files are produced. The naming convention for the report file is as follows:
	"REP_"+RID+."XML"
	This format allows to keep the results of all studies.

	The second report name:
	Proteins.XML
	It contains the same information as the first one, but is used as a generic input for step 3. 

Step 3.
Processes the study to produce the list of homolog candidates
This step compresses a big and detailed XML file to a simple text list that contains only protein names
Input
	Proteins.XML - contains homolog candidates in an expanded XML format
Output
	Homologs.txt - contains a list of homolog candidates in a simple text list form

Step 4.
Uses the names of homolog candidates to submit study requests for them, but no more than some maximum number of studies to avoid bombarding the NCBI website
Input
	Homologs.txt - contains a list of homolog candidates in a simple text list form
Output
	HOMOLOG_RIDS.txt - contains the study IDs (RIDs) that can be used to retireve the study results later.
Step 4 is very similar to Step 1, except the protein names are provided externally and not within the program. Also on Step 4 multiple study requests can be submitted.

Step 5.
Retieves the results of the studis for all RIDs given in RIDs.txt
Input
	HOMOLOG_RIDS.txt 
Output 
	Report files are produced. The naming convention for the report file is as follows:
	"REP_"+RID+."XML"
	This format allows to keep the results of all studies.
Step 5 is very similar to step 2, except it checks multiple studies

Step 6.
Takes in the report files for all studies and produces the list of all pairs
Input
	All reprot files that were produced at the previous steps. The program chels all the files that fit the following pattern:
	"REP_*.XML"

Output
	All_Pairs.txt - contains all protein pairs from all studies


The NCBI site is not very stable, some requests result in a "Bad Gateway" message. So steps should be repeated if necessary.
One should wait for NCBI to complete studies for 10-15 minutes before going to Step 2, and for up to 1 hour to complete studies before going to Step 5. 

The studies stay on the server for 36 hours


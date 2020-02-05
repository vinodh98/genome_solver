import csv

csv_file = open("results.csv", "r")
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
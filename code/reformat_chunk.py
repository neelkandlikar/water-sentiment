import csv

with open("../data/abstracts_chunk_1.csv", "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter=",", quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        # dicts_found = 0
        # new_row = []
        # ordered_dicts = [[]]
        # found_ordered = False
        # for i in range (0,len(row)):
        #     if "OrderedDict" in row[i]:
        #         for j in range(i, len(row)):
        #             if ")]))" in row[j]:
        #                 print(j)
        #                 ordered_dicts[dicts_found].append(row[j])
        #                 new_row.append(str(ordered_dicts[dicts_found]))
        #                 dicts_found = dicts_found+1
        #                 i = j+1
        #                 break
        #             ordered_dicts[dicts_found].append(row[j])
        #     else:
        #         new_row.append(row[i])
        #
        # print(new_row)
        print(row[45])





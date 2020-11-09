with open("list_of_aquifer_names_usgs.txt", "r") as in_file, open("list_of_aquifer_names_usgs_removed_paren.txt", "w") as out_file:
    for line in in_file:
        lineSplit = line.split(" (")[0]
        lineSplit.replace("\n", "")
        lineSplit += "\n"
        if len(lineSplit) >= 2:
            out_file.write(lineSplit)

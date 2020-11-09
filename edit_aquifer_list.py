with open("paper_aquifers.txt", "r") as in_file, open("modified_paper_aquifers.txt", "w") as out_file:
    for line in in_file:
        line = line.split("\t")[-1]
        if "Aquifer" in line:
            line = line.split("Aquifer")[0][:-1]
        if "Basin" in line:
            line = line.split("Basin")[0][:-1]
        out_file.write(line + "\n")
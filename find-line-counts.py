counts = set()
with open ( "/Users/burkej24/Desktop/chia_database/chia.working_models.pep.tsv" , "r" ) as in_tsv :
    for line in in_tsv:
        line = line.rstrip().split("\t")
        counts.add(len(line))
    print(counts)
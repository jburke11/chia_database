counts = set()
with open ( "/Users/burkej24/Desktop/chia_database/chia.pfam" , "r" ) as in_tsv :
    for line in in_tsv:
        line = line.rstrip().split()
        counts.add(line[0])
    print(len(counts))
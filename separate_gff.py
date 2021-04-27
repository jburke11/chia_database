big_dict = {}
with open("/Users/burkej24/Desktop/catnip/catnip_data/officinalis/h_officinalis.working.gene_models.gff3") as in_gff:
    for line in in_gff:
        lst = line.rstrip().split()
        if lst[0] in big_dict:
            big_dict[lst[0]].append(lst)
        elif lst[0] not in big_dict:
            big_dict[lst[0]] = []
            big_dict[lst[0]].append(lst)
        else:
            raise ValueError
    for key, items in big_dict.items():
        filename = "OFF-" + key + ".gff3"
        fp = open(("/Users/burkej24/Desktop/intermine_test/biotestmine-bio-sources/officinalis-gff" + filename), "w")
        for item in items:
            print("\t".join(item), file=fp)


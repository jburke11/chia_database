with open("/Users/burkej24/Desktop/catnip/catnip_data/officinalis/officinalis.pfam", "r") as teak_pfam_in:
    fp = open("/Users/burkej24/Desktop/catnip/catnip_data/officinalis/officinalis_pfam.tsv", "w")
    teak_pfam_in.readline()
    teak_pfam_in.readline ( )
    teak_pfam_in.readline ( )
    for line in teak_pfam_in:
        line = line.rstrip().split()
        description = " ".join(line[22:])
        new_line_lst = line[:22]
        new_line_lst.append(description)

        if float(line[6]) < 1e-5:
            print("\t".join(new_line_lst), file=fp)
        else:
            pass
    fp.close()
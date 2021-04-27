from Bio import SeqIO
with open ( "/Users/burkej24/Desktop/catnip/catnip_data/officinalis/h_officinalis_assembly.fa" , "r" ) as in_file :
    for record in SeqIO.parse(in_file, "fasta"):
        filename = record.id + ".fasta"
        fp = open(("/Users/burkej24/biotestmine-sample-data/officinalis/genome/fasta/" + "OFF-" + filename), "w")
        SeqIO.write(record, fp, "fasta")
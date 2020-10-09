import pymongo, gridfs
from Bio import SeqIO
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
fs = gridfs.GridFS(db)

for record in SeqIO.parse("/Users/burkej24/Desktop/chia_database/chia.final_asm.fa", "fasta"):
    seq = str(record.seq)
    chr = record.id
    file = open ( chr , "w" )
    with fs.new_file(filename=chr) as fp:
        seq = seq.encode()
        fp.write(seq)

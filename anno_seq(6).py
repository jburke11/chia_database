import pymongo
from Bio import SeqIO
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes
cdna = 0
cds = 0
pep = 0
for record in SeqIO.parse("/Users/burkej24/Desktop/chia_database/chia.working_models.cds.fa", "fasta"):
    collection.update_one ( { "transcript_id" : record.id } , { "$set" : { "cds" : str(record.seq) } } )
    cds += 1
print(cds == 59062)

for record in SeqIO.parse("/Users/burkej24/Desktop/chia_database/chia.working_models.cdna.fa", "fasta"):
    collection.update_one ( { "transcript_id" : record.id } , { "$set" : { "cdna" : str ( record.seq ) } } )
    cdna += 1
print ( cdna == 59062 )
for record in SeqIO.parse("/Users/burkej24/Desktop/chia_database/chia.working_models.pep.fa", "fasta"):
    collection.update_one ( { "transcript_id" : record.id } , { "$set" : { "protein" : str ( record.seq ) } } )
    pep += 1
print ( pep == 59062 )
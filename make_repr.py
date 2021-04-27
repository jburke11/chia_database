import pymongo
from Bio import SeqIO

# get the client
client = pymongo.MongoClient ( )
db = client.officinalis
collection = db.genes

gene_dict = collection.find({}, {"_id": 0, "gene_id": 1})
gene_set = set()
for item in gene_dict:
    gene_set.add(item["gene_id"])
print(len(gene_set))

x = 0
for item in gene_set:
    gene_dict = collection.find({"gene_id": item}, {"_id": 0})
    length = 0
    largest_transcript = ""
    for item in gene_dict:
        if len(item["cds"]) > length:
            largest_transcript = item["transcript_id"]
        else:
            pass
    x += 1
    print(x)
    collection.update_one({"transcript_id": largest_transcript}, {"$set": {"is_repr": 1}})



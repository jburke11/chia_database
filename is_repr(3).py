import pymongo
import datetime
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes
count = 0
with open("chia.gene_models.hc.repr.gene_model.list.txt") as in_genes:
    for line in in_genes:
        line = line.rstrip().split("\t")
        collection.update_one({ "transcript_id" : line[0] }, {"$set": {"is_repr": 1}})
        count += 1
print (count == 35480)
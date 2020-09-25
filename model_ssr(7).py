import pymongo
from Bio import SeqIO
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes
ssr_dict = {}
with open("ssr.tsv", "r") as in_ssr:
    for line in in_ssr:
        line = line.rstrip().split()
        data = {"end5": line[5], "end3": line[6], "unit_size": line[2], "motif": line[3], "ssr_length": line[4] }
        if line[0] in ssr_dict:
            ssr_dict[line[0]].append(data)
        else:
            ssr_dict[line[0]] = [data]
for id, data in ssr_dict.items():
    collection.update_one ( { "transcript_id" : id } , { "$set" : { "ssr" : data } } )

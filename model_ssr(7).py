import pymongo
from Bio import SeqIO
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.chia_ssr
ssr_dict = {}
with open("ssr.tsv", "r") as in_ssr:
    for line in in_ssr:
        line = line.rstrip().split()
        data = {"end5": int(line[5]), "end3": int(line[6]), "unit_size": int(line[2]), "motif": line[3], "ssr_length": int(line[4]), "scaffold": line[0] }
        collection.insert_one(data)


import pymongo
import datetime
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes
count = 0

with open("chia.working_models.func_anno.txt") as in_func:
        for line in in_func:
            line = line.rstrip().split("\t")
            collection.update_one ( { "transcript_id" : line [0] } , { "$set" : { "func_anno" : line[1] } } )
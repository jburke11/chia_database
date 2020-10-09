import pymongo
from datetime import datetime

# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes
time = datetime.now()
result = collection.find({"model_go.go_name": {"$regex":"kinase" }}, {"model_go.go_name": 1, "transcript_id": 1})

print(datetime.now() - time)


import pymongo
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes

fp = open( "/Users/burkej24/Desktop/chia_database/genes.txt" , "r" )
count = 0
for line in fp:
    data = {"transcript_id": line[1:].rstrip()}
    collection.insert_one(data)
    count += 1
    print("Gene inserted")
print(59062 == count)
import pymongo
import datetime
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes
time = datetime.datetime.now()
hc_models = []
with open("/Users/burkej24/Desktop/chia_database/chia.gene_models.hc.gff3") as hc_gff:
    for line in hc_gff:
        lst = line.rstrip().split()
        if lst [2] == "mRNA" :
            description = lst [-1]
            desc_list = description.split ( ";" )
            transcript_id = desc_list [0].split ( "=" ) [-1]
            hc_models.append(transcript_id)


count = 0
with open("/Users/burkej24/Desktop/chia_database/chia.working_models.gff3") as in_gff:
    for line in in_gff:
        lst = line.rstrip().split()
        if lst[2] == "mRNA":
            scaffold = lst[0]
            origin = lst[6]
            start = lst[3]
            stop = lst[4]
            description = lst[-1]
            desc_list = description.split(";")
            transcript_id = desc_list[0].split("=")[-1]
            gene_id = desc_list[2].split("=")[-1]
            if transcript_id in hc_models:
                collection.update_one ( { "transcript_id" : transcript_id } ,
                                        { "$set" : { "scaffold" : scaffold , "origin" : origin , \
                                                     "start" : int(start) , "stop" : int(stop) , "description" : description , \
                                                     "gene_id" : gene_id, "hc": 1 } } )
                count += 1
                print("updated document", transcript_id)
            else:
                collection.update_one({"transcript_id": transcript_id},{"$set": {"scaffold": scaffold, "origin": origin, \
                                                                    "start": int(start), "stop": int(stop), "description": description,\
                                                                    "gene_id": gene_id, "hc": 0}})
                print("updated document", transcript_id)
                count += 1
        else:
            print("passed")
            pass
print (datetime.datetime.now() - time)
print(count)
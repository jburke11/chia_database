import pymongo
import datetime
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes

with open("/Users/burkej24/Desktop/chia_database/diamond_results.tsv", "r") as in_file:
    line = in_file.readline().rstrip().split("\t")
    while line:
        gene = line [0]
        diamond_list = []
        for i in range(10):
            if gene == line[0] and line:
                data = {"accession": line[1], "per_sim": line[2], "per_cov" : line[13],"pvalue" : line[10], "description": line[12] }
                diamond_list.append(data)
                line = in_file.readline().rstrip().split("\t")
            else:
                break
        while gene == line[0] and line:
            line = in_file.readline().rstrip().split("\t")
        collection.update_one ( { "transcript_id" : gene } , { "$set" : { "diamond_results" : diamond_list } } )
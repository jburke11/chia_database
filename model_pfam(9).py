import pymongo
import datetime
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes
x = 0
with open("chia.pfam", "r") as in_pfam:
    line = in_pfam.readline( ).rstrip( ).split ()
    while line:
        gene = line[0]
        pfam_list = []
        while line[0] == gene:
            print(line)
            data = {"protein_match_start": line[1], "protein_match_end":line[2],"hmm_acc" : line[5], "hmm_match_start": int(line[8])
                    , "hmm_name": line[6],"hmm_match_end" : int(line[9]), "hmm_type" : line[7], "bit_score" : line[11], "evalue": line[12] }
            pfam_list.append(data)
            line = in_pfam.readline ( ).rstrip ( ).split ()
            print(x)
            x+=1
        collection.update_one ( { "transcript_id" : gene } , { "$set" : { "model_pfam" : pfam_list } } )

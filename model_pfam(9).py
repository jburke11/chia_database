import pymongo
import datetime
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes

with open("DM_v6_1.working_models.pep.all.sort.pfam", "r") as in_pfam:
    line = in_pfam.readline ( ).rstrip ( ).split ( "\t" )
    while line:
        gene = line[0]
        pfam_list = []
        while line[0] == gene:
            data = {"protein_match_start": line[1], "protein_match_end":line[2],"hmm_acc" : line[5], "hmm_match_start": line[8]
                    , "hmm_name": line[6],"hmm_match_end" : line[9], "hmm_type" : line[7], "bit_score" : line[11], "evalue": line[12] }
            pfam_list.append(data)
            line = in_pfam.readline ( ).rstrip ( ).split ( "\t" )
        collection.update_one ( { "transcript_id" : gene } , { "$set" : { "model_pfam" : pfam_list } } )

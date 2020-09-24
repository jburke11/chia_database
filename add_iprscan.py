import pymongo
import datetime
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes
time = datetime.datetime.now()

go_dict = {}
with open("go_slim.txt", "r") as go_in:
    go_in.readline()
    go_in.readline ( )
    go_in.readline ( )
    go_in.readline ( )
    for line in go_in:
        temp_dict = {}
        line = line.rstrip().split("\t")
        temp_dict["go_accession"] = line[5]
        temp_dict["go_type"] = line[7]
        temp_dict["go_name"] = line[8]
        temp_dict["go_ev_code"] = line[9]
        temp_dict["go_dbxref"] = "TAIR:" + line[0]
        go_dict[line[5]] = temp_dict
print("dictionary created")

count = 0
with open ( "/Users/burkej24/Desktop/chia_database/chia.working_models.pep.tsv" , "r" ) as in_tsv :
    for line in in_tsv :
        line = line.rstrip().split()
        gene = line[0]
        ipr_list = []
        while line[0] == gene:
            if len(line) == 11:
                data = {"method": line[3], "method_accession": line[4], "method_description": line[5], "match_start": line[6],
                        "match_end": line[7], "evalue":line[8], "interpro_accession": "N/A", "interpro_description": "N/A", "interpro_go": "N/A"}
            elif len(line) == 13:
                data = { "method" : line [3] , "method_accession" : line [4] , "method_description" : line [5] ,
                         "match_start" : line [6] ,
                         "match_end" : line [7] , "evalue" : line [8] , "interpro_accession" : line[12] ,
                         "interpro_description" : line[13] , "interpro_go" : "N/A" }
            elif len(line) == 14:
                data = { "method" : line [3] , "method_accession" : line [4] , "method_description" : line [5] ,
                         "match_start" : line [6] ,
                         "match_end" : line [7] , "evalue" : line [8] , "interpro_accession" : line [12] ,
                         "interpro_description" : line [13] , "interpro_go" : line[14].rstrip().split("|") }
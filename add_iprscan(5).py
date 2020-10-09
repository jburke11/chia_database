import pymongo
import datetime
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the chia database
db = client.chia
collection = db.genes
time = datetime.datetime.now()

go_dict = {}
with open("/Users/burkej24/Desktop/chia_database/go_slim.txt", "r") as go_in:
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
go_not_found = 0
count = 0
with open ( "/Users/burkej24/Desktop/chia_database/chia.working_models.pep.tsv" , "r" ) as in_tsv :
    line = in_tsv.readline().rstrip().split("\t")
    while line :
        gene = line[0]
        ipr_list = []
        go_list = []
        while line[0] == gene:
            print(count, line[0])
            if len(line) == 11:
                data = {"method": line[3], "method_accession": line[4], "method_description": line[5], "match_start": int(line[6]),
                        "match_end": int(line[7]), "evalue":line[8], "interpro_accession": "N/A", "interpro_description": "N/A", "interpro_go": "N/A"}
                ipr_list.append(data)
            elif len(line) == 13:
                data = { "method" : line [3] , "method_accession" : line [4] , "method_description" : line [5] ,
                         "match_start" : int(line [6]) ,
                         "match_end" : int(line [7]) , "evalue" : line [8] , "interpro_accession" : line[11] ,
                         "interpro_description" : line[12] , "interpro_go" : "N/A" }
                ipr_list.append(data)
            elif len(line) == 14:
                try:
                    go_terms = line[13].rstrip().split("|")
                    for item in go_terms:
                        go_list.append(go_dict[item])
                except KeyError:
                    go_not_found += 1
                data = { "method" : line [3] , "method_accession" : line [4] , "method_description" : line [5] ,
                         "match_start" : int(line [6]) ,
                         "match_end" : int(line [7]) , "evalue" : line [8] , "interpro_accession" : line [11] ,
                         "interpro_description" : line [12] }
                ipr_list.append(data)
            line = in_tsv.readline().rstrip().split("\t")
            count += 1
        collection.update_one ( { "transcript_id" : line [0] } , { "$set" : { "model_iprscan" : ipr_list, "model_go": go_list } } )

    print (count == 638748)
    print (go_not_found, "go terms not found in go slim")
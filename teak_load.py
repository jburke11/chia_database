import pymongo
from Bio import SeqIO
# get the client
client = pymongo.MongoClient()
# connect to the genes collection in the teak database
db = client.teak
collection = db.genes
try:
    """
    fp = open( "/Users/burkej24/Desktop/teak/teak_data/teak.genes_list.txt" , "r" )
    count = 0
    for line in fp:
        data = {"transcript_id": line[1:].rstrip()}
        collection.insert_one(data)
        count += 1
    if 51956 == count:
        print ( "transcript IDs loaded" )
    else:
        raise IndexError
    ############
    #start annotation data entry
    hc_models = []
    with open ( "/Users/burkej24/Desktop/teak/teak_data/teak_hc_models.gff" ) as hc_gff :
        for line in hc_gff :
            lst = line.rstrip ( ).split ( )
            if lst [2] == "mRNA" :
                description = lst [-1]
                desc_list = description.split ( ";" )
                transcript_id = desc_list [0].split ( "=" ) [-1]
                hc_models.append ( transcript_id )

    count = 0
    with open ( "/Users/burkej24/Desktop/teak/teak_data/teak_working_models.gff" ) as in_gff :
        for line in in_gff :
            lst = line.rstrip ( ).split ( )
            if lst [2] == "mRNA" :
                scaffold = lst [0]
                origin = lst [6]
                start = lst [3]
                stop = lst [4]
                description = lst [-1]
                desc_list = description.split ( ";" )
                transcript_id = desc_list [0].split ( "=" ) [-1]
                gene_id = desc_list [1].split ( "=" ) [-1]
                if transcript_id in hc_models :
                    collection.update_one ( { "transcript_id" : transcript_id } ,
                                            { "$set" : { "scaffold" : scaffold , "origin" : origin , \
                                                         "start" : int ( start ) , "stop" : int ( stop ) ,
                                                         "description" : description , \
                                                         "gene_id" : gene_id , "hc" : 1 } } )
                    count += 1
                    print ( "updated document" , transcript_id )
                else :
                    collection.update_one ( { "transcript_id" : transcript_id } ,
                                            { "$set" : { "scaffold" : scaffold , "origin" : origin , \
                                                         "start" : int ( start ) , "stop" : int ( stop ) ,
                                                         "description" : description , \
                                                         "gene_id" : gene_id , "hc" : 0 } } )
                    print ( "updated document" , transcript_id )
                    count += 1
            else :
                print ( "passed" )
                pass
    print("annotation added")

###############################################
    #start is repr
    count = 0
    with open ( "/Users/burkej24/Desktop/teak/teak_data/rep_models.txt" ) as in_genes :
        for line in in_genes :
            line = line.split(" ")[0][1:]
            print(line)
            collection.update_one ( { "transcript_id" : line } , { "$set" : { "is_repr" : 1 } } )
            count += 1
    if count != 31168 :
        raise TimeoutError
    print("representative transcripts flagged")
    """
    """
##############################################
    # start func anno
    with open ( "/Users/burkej24/Desktop/teak/teak_data/rep_models.txt" ) as in_func :
        collection.update_many({}, { "$set" : { "func_anno" : " " }})
        for line in in_func :
            line = line.split(" ")
            collection.update_one ( { "transcript_id" : line [0][1:] } , { "$set" : { "func_anno" : " ".join(line [1:]).rstrip() } } )
    print("functional annotation added")
##############################################

    # start iprscan

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
    with open ( "/Users/burkej24/Desktop/teak/teak_data/teak.working_models.pep.tsv" , "r" ) as in_tsv :
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

    #############################################################
    # add in the sequences
    cds = 0
    cdna = 0
    pep = 0

    for record in SeqIO.parse ( "/Users/burkej24/Desktop/teak/teak_data/teak.cds.fa" , "fasta" ) :
        collection.update_one ( { "transcript_id" : record.id } , { "$set" : { "cds" : str ( record.seq ) } } )
        cds += 1
    print ( cds == 51956 )

    for record in SeqIO.parse ( "/Users/burkej24/Desktop/teak/teak_data/teak.cdna.fa" , "fasta" ) :
        collection.update_one ( { "transcript_id" : record.id } , { "$set" : { "cdna" : str ( record.seq ) } } )
        cdna += 1
    print ( cdna == 51956 )
    for record in SeqIO.parse ( "/Users/burkej24/Desktop/teak/teak_data/teak.pep.fa" , "fasta" ) :
        collection.update_one ( { "transcript_id" : record.id } , { "$set" : { "protein" : str ( record.seq ) } } )
        pep += 1
    print ( pep == 51956 )
    print("sequences added")
#########################################
# add in the ssrs
    ssr_dict = { }
    collection = db.ssr
    with open ( "/Users/burkej24/Desktop/teak/teak_data/teak_ssr.tsv" , "r" ) as in_ssr :
        for line in in_ssr :
            line = line.rstrip ( ).split ( )
            data = { "end5" : int ( line [5] ) , "end3" : int ( line [6] ) , "unit_size" : int ( line [2] ) ,
                     "motif" : line [3] , "ssr_length" : int ( line [4] ) , "scaffold" : line [0] }
            collection.insert_one ( data )
    print ("ssrs added")
#########################################
# add in the diamond analysis
    collection = db.genes
    with open ( "/Users/burkej24/Desktop/teak/teak_data/diamond_results_teak.tsv" , "r" ) as in_file :
        line = in_file.readline ( ).rstrip ( ).split ( "\t" )
        while line :
            gene = line [0]
            diamond_list = []
            for i in range ( 10 ) :
                if gene == line [0] and line :
                    data = { "accession" : line [1] , "per_sim" : line [2] , "per_cov" : line [13] ,
                             "pvalue" : line [10] , "description" : line [12] }
                    diamond_list.append ( data )
                    line = in_file.readline ( ).rstrip ( ).split ( "\t" )
                else :
                    break
            while gene == line [0] and line :
                line = in_file.readline ( ).rstrip ( ).split ( "\t" )
            collection.update_one ( { "transcript_id" : gene } , { "$set" : { "diamond_results" : diamond_list } } )
    print("diamond analysis added")
#######################################
# add in pfam
    """
    x = 0
    with open("/Users/burkej24/Desktop/teak/teak_data/teak_pfam.tsv", "r") as in_pfam:
        line = in_pfam.readline( ).rstrip( ).split ("\t")
        print(line)
        while line:
            gene = line[3]
            pfam_list = []
            while line[3] == gene:
                print(line)
                data = {"protein_match_start": int(line[17]), "protein_match_end":int(line[18]),"hmm_acc" : line[1], "hmm_match_start": int(line[15])
                        , "hmm_name": line[-1],"hmm_match_end" : int(line[16]), "hmm_type" : "Domain", "bit_score" : line[7], "evalue": line[6] }
                pfam_list.append(data)
                line = in_pfam.readline ( ).rstrip ( ).split ("\t")
                print(x)
                x+=1
            collection.update_one ( { "transcript_id" : gene } , { "$set" : { "model_pfam" : pfam_list } } )
    print("pfam added")
    print("pipeline done")
except IndexError:
    print("error loading transcript Ids")

except TimeoutError:
    print("error loading repr")




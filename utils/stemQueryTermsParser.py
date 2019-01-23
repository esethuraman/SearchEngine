
def stemQueryTermsParser(source_stem_query,destination_stem_query):
    qid = 1
    with open(destination_stem_query, 'w+') as out_file:
        with open(source_stem_query, 'r') as in_file:
            for line in in_file:
                out_file.write(str(qid)+" "+ line.strip('\n') + '\n')
                qid+=1

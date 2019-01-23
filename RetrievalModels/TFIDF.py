from math import log
import operator

MAX_HIT_COUNT = 100
OUTPUT_INDEX_PATH = "../Files/Output/Ranking/"


def TFIDF(rawIndexFilename, tokenFilename, queryFilename, system_name):
    ranked_docs = []

    # Reaad the index file
    with open(rawIndexFilename, "r", encoding='utf8') as indexFile:
        index = eval(indexFile.read())

    # Read the oken information file. This file contains information about
    # the number of words present in each doc in the vocabulory
    with open(tokenFilename, "r", encoding='utf8') as tokenFile:
        tokenInfo = eval(tokenFile.read())

    # open the query file
    f = open(queryFilename, 'r')

    # Read all query lines from a query file
    queryLines = f.readlines()

    for qterm in queryLines:
        qwords = qterm.strip().split()
        ranked_docs.append(tfidf_calculate(qwords[0], qwords[1:], tokenInfo, index))

    print_results(ranked_docs, system_name)
    return ranked_docs

#Print results to the file
def print_results(result_lists, system_name):
    file_contents = ""
    for qid, result_list in result_lists:
        rank = 1
        for result in result_list:
            file_contents += str(qid) + " " + "Q0" + " " + result[0] + " " + str(rank) + " " + str(
                result[1]) + " " + system_name + "\n"
            rank += 1
        file_contents += "\n"

    print(file_contents)
    # Write ranked docs list to file
    with open(OUTPUT_INDEX_PATH + system_name + ".txt", "w", encoding='utf8') as qfile:
        qfile.write(file_contents)
    return


def tfidf_calculate(qid, qwords, tokenInfo, index):
    rankDict = {}
    for qword in qwords:
        if qword in index:
            for docId, posl in index[qword].items():
                if docId not in rankDict:
                    #doc score = tf * idf
                    rankDict[docId] = (len(posl) / tokenInfo[docId]) * log(len(tokenInfo) / (len(index[qword])))
                else:
                    rankDict[docId] += (len(posl) / tokenInfo[docId]) * log(len(tokenInfo) / (len(index[qword])))

    sortedScoreList = sorted(rankDict.items(), key=operator.itemgetter(1), reverse=True)
    return qid, sortedScoreList[:MAX_HIT_COUNT]


#Calculates the tf.idf for every word in the doc
# output : {word : tfidf_score , word1 : tfidf_score}
def tfidf_doc(docid, doc_content, index, token_dict):
    tfidf_rank = {}

    for word in doc_content:
        if word in index:
            if word not in tfidf_rank:
                tfidf_rank[word] = tfidf_score(docid, word, token_dict, index)
            else:
                tfidf_rank[word] += tfidf_score(docid, word, token_dict, index)

    return tfidf_rank


# output: tfidf_score(int)
def tfidf_score(docid_given, word, tokenDict, index):
    score = 0

    for docid, posl in index[word].items():
        score = (len(posl) / tokenDict[docid_given]) * log(len(tokenDict) / (len(index[word])))
    return score

import math
import operator

#Constants
k1 = 1.2
b = 0.75
k2 = 100
MAX_HIT_COUNT = 100
OUTPUT_RANKING_PATH = "../Files/Output/Ranking/"


def BM25(rawIndexFilename, tokenFilename,queryFilename,system_name):
    #queryFilename = input("Enter the FULL path to the query file\n")

    #open the query file
    f = open(queryFilename,'r')

    #Read the unigram tokens info from the file (From assignment 3)
    tokenDict = dict()

    #token file name: .../TokenCount-1gram(s).txt
    #tokenFilename = input("Enter the FULL path to the Token information file (HW3)\n")
    with open(tokenFilename,"r",encoding='utf8') as tokenFile:
        tokenDict = eval(tokenFile.read())

    #calculating avdl (average doc length) for unigram tokens
    avdl = sum(tokenDict.values())/len(tokenDict)

    #read the index. Index is a python dictionary directly written onto disk
    #Makes reading back the index into the memory easy

    #raw index file name: .../rawIndex-1gram(s).txt
    #rawIndexFilename = input("Enter the FULL path to the Raw index file (HW3)\n")
    with open(rawIndexFilename,"r",encoding='utf8') as indexFile:
        indexDict = eval(indexFile.read())

    #Read all query lines from a query file
    queryLines = f.readlines()
    #rankedDocsStr = "query_id Q0 doc_id rank BM25_score system_name\n"
    rankedDocs = []
    #Each query line is assumed to be of the form: query_id query_text
    #Ex: 1. hurricane isabel damage
    for q in queryLines:
        qwords = q.strip().split()
        # Calculate BM25 score for every document on every query
        rankedDocs.append(BM25_calculate(qwords[0],qwords[1:],tokenDict,indexDict,avdl))

    print_results(rankedDocs,system_name)
    return rankedDocs

#print the results to a file in the following format:
#query_id Q0 doc_id rank BM25_score system_name
def print_results(result_lists,system_name):
    file_contents = ""
    for qid,result_list in result_lists:
        rank=1
        for result in result_list:
            file_contents += str(qid) + " " + "Q0" + " " + result[0] + " " + str(rank) + " " + str(
                result[1]) + " " + system_name + "\n"
            rank+=1
        file_contents += "\n"
    print(system_name+" results:\n")
    print(file_contents)
    # Write ranked docs list to file
    with open(OUTPUT_RANKING_PATH+system_name+ ".txt", "w", encoding='utf8') as qfile:
        qfile.write(file_contents)
    return


'''
BM25: Uses BM25 algorithm to rank documents for query words
RETURNS: a string containing ranked documents for the given query (qwords)
         in decreasing order of their BM25 scores
'''
def BM25_calculate(qid, qwords,tokenDict,indexDict,avdl):
    #total number of docs
    N = len(tokenDict)

    qcount = dict()
    bm25scoresdict = dict()

    #generate query term frequency
    for qword in qwords:
        if qword not in qcount:
            qcount[qword] = 1
        else:
            qcount[qword]+= 1

    scoreDict = dict()

    for qword in qwords:
            if qword in indexDict:
                #Number of docs that contain the qword
                ni = len(indexDict[qword])

                #Frequency of qword in the query
                qfi = qcount[qword.lower()]

                #for every doc in the posting of a inverted list entry
                for docname,fi in indexDict[qword].items():
                    #Constant K
                    K = k1 * ((1 - b) + b * (tokenDict[docname] / avdl))

                    #The BM25 formula is simplified by substituting zero for relevance terms
                    val1 = 1/((ni + 0.5) / (N - ni + 0.5))
                    val2 = ((k1+1) * len(fi)) / (K + len(fi))
                    val3 = ((k2+1) * qfi) / (k2 + qfi)

                    #calculate the score. Natural logarithms
                    score = math.log(val1, math.e) * val2 * val3
                    #Calculated the score for the doc for the first time
                    if docname not in scoreDict:
                        scoreDict[docname] = score
                    #add the score to the previously calculated score
                    else:
                        scoreDict[docname] += score

    #Sort the scores in descending order
    sortedScoreList = sorted(scoreDict.items(), key=operator.itemgetter(1), reverse=True)
    return qid, sortedScoreList[:MAX_HIT_COUNT]

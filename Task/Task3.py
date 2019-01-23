# This Program produces the 6 baseline runs specified for task 3:
# BM25 with stopped corpus and with stemmed corpus
# TFIDF with stopped corpus and with stemmed corpus
# BM25 with stopped corpus and with stemmed corpus
# Query Likelihood Model with stopped corpus and with stemmed corpus

from Indexer.Indexer import make_index
from Indexer.DocumentsTermParser import parse_documents
from RetrievalModels.BM25 import BM25
from RetrievalModels.QueryLikelihoodModel import QLM
from utils.TokenInformation import generate_token_information
from Indexer.QueryTermsParser import parse_query_terms
from RetrievalModels.TFIDF import TFIDF
from utils.stemQueryTermsParser import stemQueryTermsParser
from utils.StopWordsFormatter import regenerate_stop_words

# Source and Destination paths

INPUT_PLAIN_CORPUS_PATH = "../Files/Input/Corpus/Plain"
OUTPUT_STOP_CORPUS_PATH = "../Files/Output/Corpus/Stopped"
INPUT_STEM_CORPUS_PATH = "../Files/Input/Corpus/Stemmed"
OUTPUT_STEMMED_CORPUS_PATH = "../Files/Output/Corpus/Stemmed"
OUTPUT_STOP_TOKENINFO_PATH = "../Files/Output/TokenInfo/stoptokeninfo.txt"
OUTPUT_STEMMED_TOKENINFO_PATH = "../Files/Output/TokenInfo/stemtokeninfo.txt"
OUTPUT_STOP_INDEX_PATH = "../Files/Output/Index/stoppedIndex.txt"
OUTPUT_STEMMED_INDEX_PATH = "../Files/Output/Index/stemmedIndex.txt"
INPUT_PLAIN_QUERY_PATH = "../Files/Input/Queries/Plain/cacm.query.txt"
OUTPUT_STOPPED_QUERY_PATH = "../Files/Output/Queries/stoppedQueries.txt"
STEMMED_QUERY_PATH = "../Files/Input/Queries/Stemmed/cacm_stem.query.txt"
OUTPUT_STEM_QUERY_PATH = "../Files/Output/Queries/stemquery.txt"
BM25_STOP_SYSTEM_NAME = "BM25_STOP_CASEFOLD_1GRAM"
BM25_STEM_SYSTEM_NAME = "BM25_STEM_CASEFOLD_1GRAM"
TFIDF_STOP_SYSTEM_NAME = "TFIDF_STOP_CASEFOLD_1GRAM"
TFIDF_STEM_SYSTEM_NAME = "TFIDF_STEM_CASEFOLD_1GRAM"
QLM_STOP_SYSTEM_NAME = "QLM_STOP_CASEFOLD_1GRAM"
QLM_STEM_SYSTEM_NAME = "QLM_STEM_CASEFOLD_1GRAM"

def main():

    # Usage
    # parse_documents(source_path, destination_path, stop_flag, stem_flag
    # Any one of the Stop or stem flags should be set

    #Parsing StopwordList
    regenerate_stop_words()

    #Generating Stopped Corpus
    parse_documents(INPUT_PLAIN_CORPUS_PATH, OUTPUT_STOP_CORPUS_PATH,True,False)

    #Generating Stopped TokenInfo
    generate_token_information(OUTPUT_STOP_CORPUS_PATH,OUTPUT_STOP_TOKENINFO_PATH)

    #Generating Index on Stopped corpus
    make_index(OUTPUT_STOP_CORPUS_PATH,OUTPUT_STOP_INDEX_PATH)

    #Generating Stopped Queries
    parse_query_terms(INPUT_PLAIN_QUERY_PATH,OUTPUT_STOPPED_QUERY_PATH,True)

    print("Generating BM25 with stopping")
    #Generating BM25 on Stopped Corpus
    BM25_stop_results = BM25(OUTPUT_STOP_INDEX_PATH,OUTPUT_STOP_TOKENINFO_PATH,OUTPUT_STOPPED_QUERY_PATH,BM25_STOP_SYSTEM_NAME)

    print("Generating TFIDF with stopping")
    #Generating TFIDF on Stopped Corpus
    TFIDF_stop_result = TFIDF(OUTPUT_STOP_INDEX_PATH,OUTPUT_STOP_TOKENINFO_PATH,OUTPUT_STOPPED_QUERY_PATH,TFIDF_STOP_SYSTEM_NAME)

    print("Generating QueryLikelyhood with Stopping")
    #Generating QLM on Stopped Corpus
    QLM_stop_result = QLM(OUTPUT_STOP_INDEX_PATH,OUTPUT_STOP_TOKENINFO_PATH,OUTPUT_STOPPED_QUERY_PATH,QLM_STOP_SYSTEM_NAME)

    #Generating Stemmed Corpus
    parse_documents(INPUT_STEM_CORPUS_PATH, OUTPUT_STEMMED_CORPUS_PATH,False,True)

    # Generating Stemmed TokenInfo
    generate_token_information(OUTPUT_STEMMED_CORPUS_PATH, OUTPUT_STEMMED_TOKENINFO_PATH)

    # Generating Index on Stemmed corpus
    make_index(OUTPUT_STEMMED_CORPUS_PATH, OUTPUT_STEMMED_INDEX_PATH)

    # Parsing stemmed queries ad assigning query IDs
    stemQueryTermsParser(STEMMED_QUERY_PATH,OUTPUT_STEM_QUERY_PATH)

    print("Generating BM25 with stemming")
    # Generating BM25 on Stopped Corpus
    BM25_stop_results = BM25(OUTPUT_STEMMED_INDEX_PATH, OUTPUT_STEMMED_TOKENINFO_PATH, OUTPUT_STEM_QUERY_PATH,
                             BM25_STEM_SYSTEM_NAME)

    print("Generating TFIDF with stemming")
    # Generating TFIDF on Stopped Corpus
    TFIDF_stem_result = TFIDF(OUTPUT_STEMMED_INDEX_PATH, OUTPUT_STEMMED_TOKENINFO_PATH, OUTPUT_STEM_QUERY_PATH,
                             TFIDF_STEM_SYSTEM_NAME)

    print("Generating QLM with stemming")
    QLM_stem_result = QLM(OUTPUT_STEMMED_INDEX_PATH, OUTPUT_STEMMED_TOKENINFO_PATH, OUTPUT_STEM_QUERY_PATH,
                          QLM_STEM_SYSTEM_NAME)

    print("Task 3 is complete")

if __name__ == '__main__':
    main()




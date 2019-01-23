# This program outputs the three baselines specified for Task 1
# BM25, TF-IDF, Smoothed Query Likelyhood Model as Retrieval models
# on the positional unigram index

from Indexer.Indexer import make_index
from Indexer.DocumentsTermParser import parse_documents
from RetrievalModels.BM25 import BM25
from utils.TokenInformation import generate_token_information
from Indexer.QueryTermsParser import parse_query_terms
from RetrievalModels.TFIDF import TFIDF
from RetrievalModels.QueryLikelihoodModel import QLM

# Source and Destination paths

INPUT_PLAIN_CORPUS_PATH = "../Files/Input/Corpus/Plain"
OUTPUT_PLAIN_CORPUS_PATH = "../Files/Output/Corpus/Plain"
OUTPUT_TOKENINFO_PATH = "../Files/Output/TokenInfo/tokeninfo.txt"
OUTPUT_INDEX_PATH = "../Files/Output/Index/index.txt"
INPUT_PLAIN_QUERY_PATH = "../Files/Input/Queries/Plain/cacm.query.txt"
OUTPUT_PLAIN_QUERY_PATH = "../Files/Output/Queries/queries.txt"
BM25_SYSTEM_NAME = "BM25_CASEFOLD_1GRAM"
TFIDF_SYSTEM_NAME = "TFIDF_CASEFOLD_1GRAM"
QLM_SYSTEM_NAME = "QLM_CASEFOLD_1GRAM"

def main():

    # Generating Plain corpus
    parse_documents(INPUT_PLAIN_CORPUS_PATH, OUTPUT_PLAIN_CORPUS_PATH,False,False)

    # Generating Plain Token information file
    generate_token_information(OUTPUT_PLAIN_CORPUS_PATH,OUTPUT_TOKENINFO_PATH)

    # Generating Index on Plain corpus
    make_index(OUTPUT_PLAIN_CORPUS_PATH,OUTPUT_INDEX_PATH)

    # Generating Plain QueryFile
    parse_query_terms(INPUT_PLAIN_QUERY_PATH,OUTPUT_PLAIN_QUERY_PATH,False)

    # Generating BM25 on Plain Corpus
    BM25_results = BM25(OUTPUT_INDEX_PATH,OUTPUT_TOKENINFO_PATH,OUTPUT_PLAIN_QUERY_PATH,BM25_SYSTEM_NAME)

    # Generating TFIDF on Plain Corpus
    TFIDF_results = TFIDF(OUTPUT_INDEX_PATH,OUTPUT_TOKENINFO_PATH,OUTPUT_PLAIN_QUERY_PATH,TFIDF_SYSTEM_NAME)

    #Generating QLM on Plain Corpus
    QLM_results = QLM(OUTPUT_INDEX_PATH,OUTPUT_TOKENINFO_PATH,OUTPUT_PLAIN_QUERY_PATH,QLM_SYSTEM_NAME)

    print("Task 1 is complete")

if __name__ == '__main__':
    main()

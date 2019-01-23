from Indexer.Indexer import make_index
from Indexer.DocumentsTermParser import parse_documents
from RetrievalModels.BM25 import BM25
from utils.TokenInformation import generate_token_information
from Indexer.QueryTermsParser import parse_query_terms
from RetrievalModels.TFIDF import tfidf_doc
import utils.CommonUtils
import operator
import os

INPUT_PLAIN_CORPUS_PATH = "../Files/Input/Corpus/Plain"
OUTPUT_PLAIN_CORPUS_PATH = "../Files/Output/Corpus/Plain"
OUTPUT_TOKENINFO_PATH = "../Files/Output/TokenInfo/tokeninfo.txt"
OUTPUT_INDEX_PATH = "../Files/Output/Index/index.txt"
INPUT_PLAIN_QUERY_PATH = "../Files/Input/Queries/Plain/cacm.query.txt"
OUTPUT_PLAIN_QUERY_PATH = "../Files/Output/Queries/queries.txt"
OUTPUT_EXPANDED_QUERY_PATH = "../Files/Output/Queries/expanded_queries.txt"
OUTPUT_RANKING_PATH = "../Files/Output/Ranking/"
INPUT_STOP_WORDS_PATH = "../Files/Input/Stoplist/common_words"
SYSTEM_NAME = "BM25_CASEFOLD_1GRAM"
SYSTEM_NAME_PRF = "BM25_CASEFOLD_PRF_1GRAM_k7_n2"

TOP_K = 7
TOP_N = 2

#Pseudo Relevance Feedback
def main():
    parse_documents(INPUT_PLAIN_CORPUS_PATH, OUTPUT_PLAIN_CORPUS_PATH, False, False)
    generate_token_information(OUTPUT_PLAIN_CORPUS_PATH, OUTPUT_TOKENINFO_PATH)
    make_index(OUTPUT_PLAIN_CORPUS_PATH, OUTPUT_INDEX_PATH)
    parse_query_terms(INPUT_PLAIN_QUERY_PATH, OUTPUT_PLAIN_QUERY_PATH, False)
    results = BM25(OUTPUT_INDEX_PATH, OUTPUT_TOKENINFO_PATH, OUTPUT_PLAIN_QUERY_PATH, SYSTEM_NAME)
    print("\nApplying Pseudo Relevance Feedback...\n")
    #Call PRF on the results of calling BM25
    PRF(results)
    print("\ndone.")


def get_cleaned_queries(query_file_path):
    with open(query_file_path, 'r', encoding='utf8') as qfile:
        return qfile.readlines()


def get_stop_words():
    with open(INPUT_STOP_WORDS_PATH, "r", encoding='utf8') as stopfile:
        return stopfile.readlines()


def get_expanded_queries(results):
    queries = get_cleaned_queries(OUTPUT_PLAIN_QUERY_PATH)

    #forward index has the doc and words present in a dict
    forward_index = get_forward_index(OUTPUT_PLAIN_CORPUS_PATH)
    index_dict = utils.CommonUtils.read_raw_file_as_dictionary(OUTPUT_INDEX_PATH)
    token_dict = utils.CommonUtils.read_raw_file_as_dictionary(OUTPUT_TOKENINFO_PATH)

    expanded_queries = []
    for qid, result in results:
        #Take the top k docs
        top_docs = result[:TOP_K]

        tfidf_dict = dict()
        expansion_terms = []

        #get the top N terms from the doc. tf.idf is used to get the top words
        for doc in top_docs:
            tfidf_dict = tfidf_doc(doc[0],forward_index[doc[0]], index_dict, token_dict)

            #Ignore stopwords. Don't consider stop words while expanding the query
            stop_words = get_stop_words()
            for stop_word in stop_words:
                stop_word = stop_word.replace("\n", "")
                if stop_word in tfidf_dict:
                    del tfidf_dict[stop_word.strip()]

            sorted_tf_idf_scores = sorted(tfidf_dict.items(), key=operator.itemgetter(1), reverse=True)

            #Select he stop n words
            top_n_words = sorted_tf_idf_scores[:TOP_N]

            for word, weight in top_n_words:
                expansion_terms.append(word)

        original_query_words = " ".join(queries[int(qid) - 1].strip().split()[1:])
        expanded_queries.append(
            str(qid) + " " + original_query_words + " " + " ".join(term for term in expansion_terms))

    return expanded_queries


def PRF(results):
    expanded_queries = get_expanded_queries(results)
    write_queries_to_text_file(OUTPUT_EXPANDED_QUERY_PATH, expanded_queries)
    #Aplly BM25 again, this time on the expanded queries
    results = BM25(OUTPUT_INDEX_PATH, OUTPUT_TOKENINFO_PATH, OUTPUT_EXPANDED_QUERY_PATH, SYSTEM_NAME_PRF)
    return results

#Write the expanded queries to file
def write_queries_to_text_file(qfile_name, query_list):
    with open(qfile_name, 'w', encoding='utf8') as qfile:
        qfile.write('\n'.join(query for query in query_list))

# returns a forward index (DocID -> Doc words)
def get_forward_index(cleaned_corpus_path):
    docsdict = dict()
    for dir_entry in os.listdir(cleaned_corpus_path):
        dir_entry_path = cleaned_corpus_path + "/" + dir_entry

        # Only if directory entry is a file, won't go through sub directories
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r', encoding="utf8",errors="ignore") as cleaned_file:
                fileContents = cleaned_file.read()
                docsdict[cleaned_file.name] = fileContents.split()

    return docsdict

if __name__ == "__main__":
    main()

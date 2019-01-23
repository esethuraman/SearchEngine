from Indexer.Indexer import make_index
from Indexer.DocumentsTermParser import parse_documents
from RetrievalModels.BM25 import BM25
from utils.TokenInformation import generate_token_information
from Indexer.QueryTermsParser import parse_query_terms
from ResultDisplay.SnippetGeneration import get_snippet
from utils.CommonUtils import get_stop_words
import re

INPUT_PLAIN_CORPUS_PATH = "../Files/Input/Corpus/Plain"
OUTPUT_PLAIN_CORPUS_PATH = "../Files/Output/Corpus/Plain"
OUTPUT_TOKENINFO_PATH = "../Files/Output/TokenInfo/tokeninfo.txt"
OUTPUT_INDEX_PATH = "../Files/Output/Index/index.txt"
INPUT_PLAIN_QUERY_PATH = "../Files/Input/Queries/Plain/cacm.query.txt"
OUTPUT_PLAIN_QUERY_PATH = "../Files/Output/Queries/queries.txt"
OUTPUT_RESULT_DISPLAY_PATH = "../Files/Output/ResultDisplay/"
BM25_SYSTEM_NAME = "BM25_CASEFOLD_1GRAM"
TFIDF_SYSTEM_NAME = "TFIDF_CASEFOLD_1GRAM"


def main():
    # Generating Plain corpus
    parse_documents(INPUT_PLAIN_CORPUS_PATH, OUTPUT_PLAIN_CORPUS_PATH, False, False)

    # Generating Plain Token information file
    generate_token_information(OUTPUT_PLAIN_CORPUS_PATH, OUTPUT_TOKENINFO_PATH)

    # Generating Index on Plain corpus
    make_index(OUTPUT_PLAIN_CORPUS_PATH, OUTPUT_INDEX_PATH)

    # Generating Plain QueryFile
    parse_query_terms(INPUT_PLAIN_QUERY_PATH, OUTPUT_PLAIN_QUERY_PATH, False)

    # Generating BM25 on Plain Corpus
    BM25_results = BM25(OUTPUT_INDEX_PATH, OUTPUT_TOKENINFO_PATH, OUTPUT_PLAIN_QUERY_PATH, BM25_SYSTEM_NAME)

    #Read the queries from the path
    queries = read_queries(OUTPUT_PLAIN_QUERY_PATH)
    querydict = dict()

    #For every query, highlight the query words from the result in the original docs
    for query in queries:
        query = query.strip()
        qterms = query.split()

        qid = qterms[0]
        qwords = qterms[1:]
        querydict[qid] = qwords

    # Each result displayed has two kinds of information:
    # The document name and
    # the snippet from the document with query words highlighted
    for qid, result_list in BM25_results:
        display_data = []
        for result in result_list:
            data_dict = dict()
            data_dict['snippet'] = highlight_snippet_with_html(get_snippet(result[0], querydict[qid]), querydict[qid],
                                                               get_stop_words()) + "</li><br/>"
            data_dict['title'] = "<li><div>" + result[0] + "</div>"
            display_data.append(data_dict)
        write_output_data_to_file(OUTPUT_RESULT_DISPLAY_PATH, display_data, qid,qwords)

    print("done")

#Results are displayed in html so that highlighting becomes easier
def write_output_data_to_file(output_path, display_data, qid,qwords):
    output_str = ""
    qwords_str = ' '.join(x for x in qwords)
    for data in display_data:
        output_str += data['title'] + data['snippet']
    heading = "<h2> Query - " + qwords_str + "</h2>"
    output_str = heading + "<ol>" + output_str + "</ol>"
    with open(output_path + str(qid) + ".html", "w") as result_display_file:
        result_display_file.write(output_str)

#Highlight all query words except stopwords. Stopwords are not significant
def highlight_snippet_with_html(content, qwords, stop_words):
    html_snippet = content
    for qword in qwords:
        if qword not in stop_words:
            html_snippet = re.sub(qword, " <b>" + qword + "</b> ", html_snippet, flags=re.IGNORECASE)
    return "<span>" + html_snippet + "</span>"

#Read formatted queries from the path
def read_queries(formatted_query_file_path):
    with open(formatted_query_file_path, 'r', encoding='utf8') as qfile:
        return qfile.readlines()

if __name__ == '__main__':
    main()

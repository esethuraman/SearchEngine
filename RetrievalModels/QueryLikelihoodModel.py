import operator
import math

from utils.MetricsCapturer import get_document_term_frequency, \
    get_collection_term_frequency

from utils import properties

tokenized_queries_file = properties.tokenized_queries_file
# this implements the Jelinek-Mercer (JM) smoothing

smoothing_coefficient = 0.35

# this dictionaty id of the form : {document_id : query_likelihood_probability}
query_likelihood_dict = {}
INPUT_PLAIN_CORPUS_PATH = "../Files/Input/Corpus/Plain"
OUTPUT_PLAIN_CORPUS_PATH = "../Files/Output/Corpus/Plain"
OUTPUT_TOKENINFO_PATH = "../Files/Output/TokenInfo/tokeninfo.txt"
OUTPUT_INDEX_PATH = "../Files/Output/Index/index.txt"
INPUT_PLAIN_QUERY_PATH = "../Files/Input/Queries/Plain/cacm.query.txt"
OUTPUT_PLAIN_QUERY_PATH = "../Files/Output/Queries/Plain/stopped_queries.txt"
OUTPUT_EXPANDED_QUERY_PATH = "../Files/Output/Queries/Plain/expanded_queries.txt"
OUTPUT_RANKING_PATH = "../Files/Output/Ranking/"
INPUT_STOP_WORDS_PATH = "../Files/Input/Stoplist/common_words"

'''
GIVEN: 
RETURNS: 
'''


def calculate_query_likelihood_score(doc_id, inv_indx_dict, query_terms, document_length_dict, collection_length):
    overall_score = 0

    for q_term in query_terms:
        document_term_frequency = get_document_term_frequency(inv_indx_dict, q_term, doc_id)
        collection_term_frequency = get_collection_term_frequency(inv_indx_dict, q_term)

        document_length = document_length_dict[doc_id]

        first_part = (1 - smoothing_coefficient)
        second_part = document_term_frequency / document_length
        third_part = smoothing_coefficient * (collection_term_frequency / collection_length)

        intermediate_value = ((first_part * second_part) + third_part)

        if intermediate_value != 0:
            intermediate_value = math.log(intermediate_value)

        overall_score += intermediate_value

    return overall_score


def construct_dictionary(document_ids, inverted_index_dict, query_terms, document_length_dict, collection_length):
    scored_dict = dict({})
    for doc_id in document_ids:
        score = calculate_query_likelihood_score(doc_id, inverted_index_dict, query_terms, document_length_dict,
                                                 collection_length)

        scored_dict[doc_id] = score
    return scored_dict

#Applies the Query Likelihood model and returns the results
def QLM(inverted_index_file, doc_length_info_file, tokenized_queries_file, SYSTEM_NAME):
    print("QLM ranking in progress ... ")
    results_list = []

    #get the inverted index from the file
    with open(inverted_index_file, "r", encoding='utf8') as indexFile:
        inverted_index_dict = eval(indexFile.read())

    #Read the token information from file. (How many tpkens are present in each doc)
    with open(doc_length_info_file, 'r', encoding='utf-8') as tokenFile:
        document_length_dict = eval(tokenFile.read())

    document_ids = document_length_dict.keys()

    collection_length = 0
    for k, v in document_length_dict.items():
        collection_length += v

    with open(tokenized_queries_file, "r") as queries_file:
        all_queries = queries_file.readlines()
        for query in all_queries:
            # ignore the first string as it is query id
            query_terms = query.split()[1:]
            query_id = query.split()[0]

            scored_dict = construct_dictionary(document_ids, inverted_index_dict, query_terms, document_length_dict,
                                               collection_length)
            sorted_list = sorted(scored_dict.items(), key=operator.itemgetter(1), reverse=True)
            sorted_list = sorted_list[1:101]
            results_list.append([query_id, sorted_list])

    # write_top_100_docs(query_id, scored_dict)
    print_results(results_list, SYSTEM_NAME)
    print("QLM ranking done...")
    return results_list


#orinting the results in the format:
#query_id Q0 doc_id rank BM25_score system_name
def print_results(result_lists, system_name):
    file_contents = ""
    for qid, result_list in result_lists:
        rank = 1
        for result in result_list:
            file_contents += str(qid) + " " + "Q0" + " " + result[0] + " " + str(rank) + " " + str(
                result[1]) + " " + system_name + "\n"
            rank += 1
        file_contents += "\n"

    # Write ranked docs list to file
    with open(OUTPUT_RANKING_PATH + system_name + ".txt", "w", encoding='utf8') as qfile:
        qfile.write(file_contents)
    return

# Testing purposes
# if __name__ == "__main__":
#     parse_documents(INPUT_PLAIN_CORPUS_PATH, OUTPUT_PLAIN_CORPUS_PATH, False, False)
#     parse_query_terms(INPUT_PLAIN_QUERY_PATH, OUTPUT_PLAIN_QUERY_PATH, True)
#     generate_token_information(OUTPUT_PLAIN_CORPUS_PATH, OUTPUT_TOKENINFO_PATH)
#     make_index(OUTPUT_PLAIN_CORPUS_PATH, OUTPUT_INDEX_PATH)
#     parse_query_terms(INPUT_PLAIN_QUERY_PATH, OUTPUT_PLAIN_QUERY_PATH, False)
#     QLM(properties.inverted_index_file, OUTPUT_TOKENINFO_PATH, OUTPUT_PLAIN_QUERY_PATH)




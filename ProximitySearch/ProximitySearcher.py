import operator

from utils import properties
from utils import CommonUtils
from ProximitySearch.ProximityScorer import get_proximity_scored_dict
from ProximitySearch.RelaxedProximitySearch import find_near_match_docs
from Evaluation.EffectivenessFinder import find_effectiveness_scores

INVERTED_INDX_FILE = properties.inverted_index_file

QUERIES_FILE = properties.queries_file

# loading the inverted index in to python dictionary
def get_inv_index_dict(file_path):
    with open(file_path, 'r') as file:
        inv_indx_dict = eval(file.readlines()[0])
        return inv_indx_dict

# for exact match, documents having strictly all query terms in
# the exact order with a max distance of 3 should be found
def get_all_terms_matched_docs(inv_indx_dict, query_terms_lst):
    all_docs_lst = []

    # { no_of_docs : term_position_in_query}
    termPos_docsCount_dict = {}

    #for accessing the list with minimum no of documents.
    # improves efficiency
    term_pos = -1

    # for each q_term get all the documents that the term is present in

    for each_term in query_terms_lst:
        key = each_term
        if key in inv_indx_dict.keys():
            docs_positions_dict = inv_indx_dict[each_term]

            term_pos += 1
            termPos_docsCount_dict[len(docs_positions_dict.keys())] = term_pos
            all_docs_lst.append(docs_positions_dict)

        else:
            # if even a single query term is not found in the collection,
            # then none of the documents in the corpus can be matched
            return []
    # print(termPos_docsCount_dict)
    sorted_tuple = sorted(termPos_docsCount_dict.items(), key=operator.itemgetter(0))
    sorted_termPos_docsCount_dict = (dict(sorted_tuple))

    # flag for storing the list having least no of docs
    all_terms_matched_docs = []
    list_of_lsts = []
    min_list_index = 0
    index_count = 0
    min_length = 99999999999999999
    for docs_count, q_term_pos in sorted_termPos_docsCount_dict.items():
        q_term_docs_lst = list(all_docs_lst[q_term_pos].keys())
        # for lst in master_lst:
        if len(q_term_docs_lst) < min_length:
            min_length = len(q_term_docs_lst)
            min_list_index = index_count
        list_of_lsts.append(q_term_docs_lst)
        index_count += 1

    # filter the docs that has all query terms
    min_length_lst = list_of_lsts[min_list_index]

    all_match_flag = True

    final_lst = []
    for doc_id in min_length_lst:
        all_match_flag = True
        for lst in list_of_lsts:
            if doc_id not in lst:
                all_match_flag = False

        if all_match_flag:
            final_lst.append(doc_id)
    return final_lst


# returns dictionary of { docid : [positions list] } for
# documents that has all terms matched from query
def get_info_for_all_matched_docs(query_terms_lst, all_match_docs, inv_indx_dict):
    docs_positions_dict = {}
    positions_lst = []
    # print("q-terms", query_terms_lst)
    for doc_id in all_match_docs:
        positions_lst = []

        for q_term in query_terms_lst:
            doc_pos_lst = inv_indx_dict[q_term][doc_id]
            positions_lst.append(doc_pos_lst)
            docs_positions_dict[doc_id] = positions_lst


    return docs_positions_dict


# system name is either stopped or unstopped
def perform_proximity_search(QUERIES_FILE, INVERTED_DICT_FILE, SYSTEM_NAME):
    OUTPUT_FILE = properties.proximity_output_path + "/Results_"+SYSTEM_NAME+".txt"
    inv_indx_dict = get_inv_index_dict(INVERTED_DICT_FILE)
    output_lst = []

    for query in CommonUtils.get_all_queries(QUERIES_FILE):

        query_terms_lst = CommonUtils.get_query_terms_lst(query)
        q_id = CommonUtils.get_q_id(query)
        # print(q_id)
        all_terms_match_docs = get_all_terms_matched_docs(inv_indx_dict, query_terms_lst)
        # if no document has all the query terms, find the nearby macthed documents

        docs_pos_dict = get_info_for_all_matched_docs(query_terms_lst, all_terms_match_docs, inv_indx_dict)
        exact_matches_dict = get_proximity_scored_dict(docs_pos_dict)

        near_match_dict = find_near_match_docs(inv_indx_dict, query_terms_lst)

        # merged_dict = {**near_match_dict, **docs_pos_dict}
        merged_dict = merge_two_dics(near_match_dict, exact_matches_dict)
        sorted_merged_tuple = sorted(merged_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_merged_tuple = sorted_merged_tuple[:100]
        # print("==>",dict(sorted_merged_tuple))
        final_scored_dict = dict(sorted_merged_tuple)
        output_lst.append([query, final_scored_dict])
        # write_results(q_id, final_scored_dict, OUTPUT_FILE)
    write_results(output_lst, OUTPUT_FILE)
    print("[INFO] Top 100 documents with scores are written in to the output file ...")
    # build_dict(output_lst)
    print("[INFO] Evaluation being performed on proximity results ...")
    find_effectiveness_scores(OUTPUT_FILE, "PROXIMITY_"+SYSTEM_NAME)
    print("[INFO] Evaluation done and the results are written to output file ...")


def write_results(output_lst, OUTPUT_FILE):
    with open(OUTPUT_FILE, 'w') as file:
        # lst[0] -> query
        for lst in output_lst:
            q_id = lst[0].split()[0]
            scored_dict = lst[1]
            for doc, score in scored_dict.items():
                file.write("\n" + q_id +" Q0 " +doc + "     "+ str(score))


# excat match and near match dictionaries are merged
# while merging, exact mactch docs are priorities as they
# have positive scores. Also for exact matches, their scores are
# boosted up with frequency scores.
def merge_two_dics(near_match_dict, exact_match_dict):

    for key in exact_match_dict.keys():
        if key in near_match_dict.keys():
            exact_match_dict[key] = exact_match_dict[key] + (-(1/near_match_dict[key]))
            # print(key, "--->" , near_match_dict[key])
    merged_dict = near_match_dict.copy()
    # replacing nearmatch values with actual match values if any
    # as exact macthes must be in the list
    merged_dict.update(exact_match_dict)
    return merged_dict


if __name__ == "__main__":
    perform_proximity_search(QUERIES_FILE, INVERTED_INDX_FILE, "PLAIN")
    perform_proximity_search(properties.stopped_queries_file, properties.stopped_inv_index_file, "STOPPED")
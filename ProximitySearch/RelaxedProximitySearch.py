import operator

def find_near_match_docs(inv_indx_dict, query_terms_lst):
    termPos_docsCount_dict, all_docs_list =  get_termPos_docsCount_dict(inv_indx_dict, query_terms_lst)
    list_of_docs_list = get_list_of_docs_list(termPos_docsCount_dict, all_docs_list)
    all_docs_list = deflate_list_of_lists_to_set(list_of_docs_list)

    # this will remove redudant documents. Hence these are the documents that
    # has at least one of the queryt terms present
    all_docs_set = set(all_docs_list)
    docs_freq_dict = get_doc_frqncy_dict(inv_indx_dict, all_docs_set, query_terms_lst)
    scored_docs_dict = get_scored_docs_dict(docs_freq_dict)

    # sort the docs based on their scores
    sorted_doc_scores_tuple = sorted(scored_docs_dict.items(), key=operator.itemgetter(1), reverse=True)

    # limit the output to just 100 documents
    sorted_doc_scores_tuple = sorted_doc_scores_tuple[:100]
    # scored_docs_dict = sorted(sorted_doc_scores_tuple, key=operator.itemgetter(1), reverse= True)

    print("[INFO] Near matches search completed...")
    return dict(sorted_doc_scores_tuple)


def get_termPos_docsCount_dict(inv_indx_dict, query_terms_lst):
    all_docs_lst = []
    termPos_docsCount_dict = {}

    term_pos = -1

    for each_term in query_terms_lst:
        key = each_term
        if key in inv_indx_dict.keys():

            docs_positions_dict = inv_indx_dict[key]

            term_pos += 1
            termPos_docsCount_dict[len(docs_positions_dict.keys())] = term_pos
            all_docs_lst.append(docs_positions_dict)

    return termPos_docsCount_dict, all_docs_lst

# returns a list of list where each inner list is a list of documents for each query term
def get_list_of_docs_list(termPos_docsCount_dict, all_docs_lst):
    list_of_docs_lst = []
    for docs_count, q_term_pos in termPos_docsCount_dict.items():
        q_term_docs_lst = list(all_docs_lst[q_term_pos].keys())
        list_of_docs_lst.append(q_term_docs_lst)

    return list_of_docs_lst


# this deflates all the documents from the list of documents list
# this will have redundant documents. Basically all the documents having any of the
# query terms will be returned by this
def deflate_list_of_lists_to_set(list_of_docs_list):

    deflated_list = []
    for inner_list in list_of_docs_list:
        deflated_list += inner_list
    return (deflated_list)

# returns a dict : { doc_id : frequency_of_all_query_terms_in_the document}
def get_doc_frqncy_dict(inv_indx_dict, all_docs_set, query_terms_lst):
    doc_frqncy_dict = {}
    for doc_id in all_docs_set:
        overall_terms_frequency = 0
        for q_term in query_terms_lst:
            if q_term in inv_indx_dict.keys():
                if doc_id in inv_indx_dict[q_term].keys():
                    this_qterm_frqncy = len(inv_indx_dict[q_term][doc_id])
                    overall_terms_frequency += this_qterm_frqncy
        doc_frqncy_dict[doc_id] = overall_terms_frequency

    sorted_dict = sorted
    return doc_frqncy_dict

# computing scores. Formula used : score = -(1/frequency)
# because, these scores must be lower than exact matched score
def get_scored_docs_dict(docs_freq_dict):
    scored_dict = {}
    for doc_id, freq in docs_freq_dict.items():
        score = -(1/freq)
        scored_dict[doc_id] = score
    return scored_dict
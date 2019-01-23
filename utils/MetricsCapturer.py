from utils import properties

index_file_path = properties.inverted_index_file
raw_corpus_path = properties.clean_corpus_path

'''
GIVEN: document's directory location and document's name (without txt extension) and the query term
RETURNS: frequency of the query term in the document
'''
def get_document_term_frequency(inv_indx_dict, term, doc_name):
    term = term.strip()
    if term in inv_indx_dict:
        if doc_name in inv_indx_dict[term]:
            return len(inv_indx_dict[term][doc_name])

    return 0

'''
GIVEN: path where all the tokenized documents are stored 
RETURNS: frequency of the query term in the collection
'''
def get_collection_term_frequency(inv_indx_dict, term):
    collection_term_frequency = 0

    if term in inv_indx_dict:
        term_dict = inv_indx_dict[term]
        for doc_id, doc_term_lst in term_dict.items():
            collection_term_frequency += len(doc_term_lst)

    return collection_term_frequency

def main():
    #testing for some docs
    print(get_document_term_frequency("preliminary", "CACM-0001"))
    print(get_document_term_frequency( 'algebraic' , "CACM-2090"))
    print(get_collection_term_frequency("preliminary"))

if __name__=="__main__":
    main()
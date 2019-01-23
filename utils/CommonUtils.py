from utils import properties

#This file has common utility functions used across the project

#Returns the stop words
def get_stop_words():
    file = open(properties.formatted_stop_words_file, 'r' )
    return (file.readlines()[0].split())

#Returns a dictionary written to file
def read_raw_file_as_dictionary(path):
    with open(path,'r',encoding='utf8') as file:
        return eval(file.read())

#Returns the query terms for a query. Ignores the query id
def get_query_terms_lst(query):
    query_terms_lst = []
    query_terms = query.split()

    # ignoring the first string as it is the query id
    query_terms = query_terms[1:]

    for q_term in query_terms:
        q_term = q_term.strip()
        if len(q_term) > 0:
            query_terms_lst.append(q_term)
    return query_terms_lst

def get_q_id(query):
    query_terms_lst = []
    query_terms = query.split()

    # ignoring the first string as it is the query id
    q_id = query_terms[0]
    return q_id


#Returns all queries in the query file
def get_all_queries(queries_file):
    with open(queries_file, 'r') as file:
        all_lines = file.readlines()
    return all_lines

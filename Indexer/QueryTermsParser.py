import os
from bs4 import BeautifulSoup
from .Parser import parse_and_tokenize

def parse_query_terms(source_file_name, destination_path, stop_flag):

    is_first_line = True
    tokenized_string = ""

    #open query file once, read all query file and process each one
    with open(os.path.join(source_file_name), 'r') as query_terms_file:
        content = query_terms_file.read().replace('\n', ' ')

    soup = BeautifulSoup(content, 'html.parser')

    # each 'doc' is a separate query
    all_queries = soup.find_all('doc')

    for query in all_queries:

        # remove the docno tag to get plain query text
        modified_query = ( ''.join(text for text in query.find_all(text=True) if text.parent.name != "docno"))

        # the query no is extracted for file creation purpose
        query_id = ((query.find('docno')).get_text())

        if is_first_line:
            is_first_line = False
        else:
            tokenized_string += "\n"

        # all the tokenized query terms are concatenated with query id in the front
        tokenized_string += query_id + " " +\
                            parse_and_tokenize(modified_query,
                                               stop_flag)

    write_in_to_file(tokenized_string, destination_path)

    print("Parsing completed.. Please look in to the destination folder for the tokenized queries")

# all the query terms are tokenized and written in to a single file called TokenizedQueries.txt
# Each line is a query term and the first string of each line is query_id for that term
def write_in_to_file(tokenized_string, destination_path):
    with open(destination_path, 'w') as file:
        file.write(tokenized_string)

#Testing purposes
# if __name__=="__main__":
#parse_query_terms("../Files/cacm.query.txt", "../Files")
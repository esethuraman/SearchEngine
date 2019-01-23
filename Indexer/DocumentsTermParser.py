import os
from bs4 import BeautifulSoup
import re
from Indexer.Parser import parse_and_tokenize

# expects two flags for stopping and stemming
def parse_documents(source_path, destination_path, stop_flag, stem_flag):
    if stem_flag:
        handler_for_stem(source_path, destination_path, stop_flag)
    else:
        handler_for_non_stem(source_path, destination_path, stop_flag)

def handler_for_non_stem(source_path, destination_path, stop_flag):
    #For every doc in the directory
    for document_name in os.listdir(source_path):

        with open(os.path.join(source_path, document_name),'r',encoding='utf8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            document_content = ""

            # only pre tags are needed
            for content in soup.find_all('pre'):
                document_content = " " + (content.text)

            # truncating the ".html" part of the document name
            document_name = document_name.replace(".html","")

            # calling the parser for tokenizing
            tokenized_string = parse_and_tokenize(document_content,
                               stop_flag)

            #Write the cleaned doc to file
            write_in_to_file(tokenized_string, destination_path, document_name)

            print("Document ", document_name, "parsed and tokenized ... ")
    print("All documents are parsed and tokenized...")

def handler_for_stem(source_path, destination_path, stop_flag):
    #For every doc in the directory
    for document_name in os.listdir(source_path):
        with open(os.path.join(source_path, document_name), 'r', encoding='utf8') as file:
            all_lines = file.readlines()

        entire_file_content = ''.join(str(element) for element in all_lines)

        # documents are delimted by # doc_id
        doc_lst = entire_file_content.split('#')

        for doc in doc_lst:
            if(len(doc.strip()) > 0):
                # parsing each document to remove digits at the last
                doc_content_lst = doc.strip().split()

                # the first string is the document id
                doc_id = doc_content_lst[0]
                doc_content_lst = doc_content_lst[1:]

                # code for removing digits at the end of document
                length = len(doc_lst)
                threshold = -(length) - 1
                digits_index = -1
                while (re.match('\d+', doc_content_lst[digits_index])) and \
                        (digits_index!=threshold):
                    doc_content_lst = doc_content_lst[:digits_index]

                # obtaining a string to feed to the parse and tokenizer
                plain_doc_content = ' '.join(str(e) for e in doc_content_lst)

                tokenized_string = parse_and_tokenize(plain_doc_content, stop_flag)

                # writin tokenized files to the output
                document_name = "Doc_"+doc_id
                write_in_to_file(tokenized_string, destination_path, document_name)
                print("Document ", document_name, "parsed and tokenized ... ")
        print("All documents are parsed and tokenized...")


#Write the given string to the given filename
def write_in_to_file(tokenized_string, destination_path, document_name):
    with open(destination_path+"/"+document_name+".txt", 'w') as file:
        file.write(tokenized_string)




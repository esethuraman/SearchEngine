import importlib.machinery

# loader = importlib.machinery.SourceFileLoader('report', parser_file_path)
# handler = loader.load_module('report')

# file that stores all the document ids
document_ids_file_name = "/Users/vihabidre/NEURelated/CS6200IR/SearchEngine/IRProject/CodeBase/DocumentIds.txt"

# file that stores the index
index_file_path = "/Users/vihabidre/NEURelated/CS6200IR/SearchEngine/IRProject/CodeBase/Index.txt"

# path where the tokenized documents are stored
destination_folder = "/Users/vihabidre/NEURelated/CS6200IR/SearchEngine/Corpus_Destination"

def get_doc_id(doc_id_path):
    docid = []
    with open(doc_id_path, "r") as file:
        for line in file:
            docid.append(line.strip())
    return docid

# GIVEN : list of Document ID
# Creating an inverted index from the doc to terms hashmap
def get_inverted_index(docid):
    tokens = tokenize_files(docid)
    total = create_index(tokens)
    inverted_index = create_full_index(total)
    return inverted_index


# Initial text filtering (parsing and tonkenizing words)
# GIVEN : List of filenames and n-gram
# RETURNS : Files after Prasing and Tokeninzing them.
# NOTE : ngrams is assumed to be 1 for this assignment.
def tokenize_files(filenames):
    file_to_terms = {}
    for file in filenames:
        file_to_terms[file] = [' '.join(x) for x in ngrams
        (open("/Users/vihabidre/NEURelated/CS6200IR/SearchEngine/Corpus_Destination/"+file+'.txt', 'r').read().replace("\n"," "), 1)]
    return file_to_terms

# GIVEN : File Contents and Option
# RETURNS : ngrams of the file contents
def ngrams(file_contents, n):
    file_contents = file_contents.split(' ')
    ngrams = []
    for i in range(len(file_contents)-n+1):
        ngrams.append(file_contents[i:i + n])
    return ngrams

# GIVEN : A map where filenames are keys and the token are the values
# RETURNS : A hashmap where filenames are keys, and map of tokens,
# term frequency are the values
def create_index(doc_ids):
    file_indexed = {}
    for filename in doc_ids.keys():
        file_indexed[filename] = index_each_file(doc_ids[filename])
    return file_indexed

# GIVEN : filename to termlist hashmap
# RETURNS : Terms to documentId hashmap
def create_full_index(file_index):
    inverted_index = {}
    for filename in file_index.keys():
        for word in file_index[filename].keys():
            if word in inverted_index.keys():
                if filename in inverted_index[word].keys():
                    inverted_index[word][filename].extend(file_index[filename][word][:])
                else:
                    inverted_index[word][filename] = file_index[filename][word]
            else:
                inverted_index[word] = {filename: file_index[filename][word]}
    return inverted_index

# GIVEN : Tokenized file contents
# RETURN : Map of the words and their term frequency.
def index_each_file(file_contents):
    fileIndex = {}
    for index, word in enumerate(file_contents):
        if word in fileIndex.keys():
            fileIndex[word] = fileIndex[word]+1
        else:
            fileIndex[word] = 1
    return fileIndex

def main():

    doc_id = get_doc_id("/Users/vihabidre/NEURelated/CS6200IR/SearchEngine/IRProject/CodeBase/DocumentIds.txt")

    # Generates a unigram index
    inverted_index = get_inverted_index(doc_id)



    with open(index_file_path, 'w') as file:
        for key,val in inverted_index.items():
            file.write(str(key)+" "+str(val)+"\n")




main()




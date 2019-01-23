import os

# returns the list of docids from dir path.
def getAllFiles(dir_path):
    # Get all the files in the dir and subdirs
    allfiles = []
    for pack in os.walk(dir_path):
        for files in pack[2]:
            if os.path.isfile(dir_path + "/" + files):
                allfiles += [dir_path + "/" + files]
    return allfiles


# Initial text filtering (parsing and tonkenizing words)
# GIVEN : List of filenames and n-gram
# RETURNS : Files after Prasing and Tokeninzing them.
# NOTE : ngrams is assumed to be 1 for this assignment.
def tokenize_files(filenames):
    file_to_terms = {}
    for file in filenames:
        file_to_terms[file] = [' '.join(x) for x in
                               ngrams(open(file, 'r', encoding='utf8', errors="ignore").read().replace("\n", " "), 1)]
    return file_to_terms


# GIVEN : File Contents and Option
# RETURNS : ngrams of the file contents
def ngrams(file_contents, n):
    file_contents = file_contents.split(' ')
    ngrams = []
    for i in range(len(file_contents) - n + 1):
        ngrams.append(file_contents[i:i+n])
    return ngrams


# GIVEN : A map where filenames are keys and the token are the values
# RETURNS : A hashmap where filenames are keys, and map of tokens,
# term frequency are the values
def create_index(doc_ids):
    file_indexed = {}
    #change happens here for filename nt path
    for filename in doc_ids.keys():
        file_indexed[filename] = index_each_file(doc_ids[filename])
    return file_indexed


# GIVEN : filename to termlist hashmap
# RETURNS : Terms to documentId hashmap
def create_full_index(file_index):
    inverted_index = {}
    for filename in file_index.keys():
        #change happens here - only file name
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
            fileIndex[word].append(index)
        else:
            fileIndex[word] = [index]
    return fileIndex


# GIVEN : list of Document ID
# Creating an inverted index from the doc to terms hashmap
def get_inverted_index(docids):
    tokens = tokenize_files(docids)
    total = create_index(tokens)
    inverted_index = create_full_index(total)
    return inverted_index

#GIVEN: index_creation_path , dictioonary containing index
#       Write the index to file
def write_index(index_creation_path, index_dict):
    with open(index_creation_path, "w", encoding='utf8',errors="ignore") as f:
        f.write(str(index_dict))


def make_index(cleaned_corpus_path, index_path):
    # Retrieve Document IDs from a text file
    doc_ids = getAllFiles(cleaned_corpus_path.strip())

    # Generates a unigram index
    inverted_index = get_inverted_index(doc_ids)

    # Write the inverted index to file
    write_index(index_path, inverted_index)

from math import log
import operator

# returns the bm 25 score
def BM25_score(n,f,qf,r,N,dl,avdl):
    k1 = 1.2
    k2 = 100
    b = 0.75
    R = 0.0
    K = k1 * ((1-b) + b * (float(dl)/float(avdl)))
    term1 = ((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5))
    term2 = ((k1 + 1) * f) / (K + f)
    term3 = ((k2 + 1) * qf) / (k2 + qf)
    score = log(term1) * term2 * term3
    return score

#returns the list of docid.
#this is retrived from a file "DocumentId.txt"
#that gets generated when downloading the corpus
# "GenerateCorpus.py" does this.
def get_doc_id():
    docid = []
    with open("DocumentIds.txt", "r") as file:
        for line in file:
            docid.append(line.strip())
    return docid

# Initial text filtering (parsing and tonkenizing words)
# GIVEN : List of filenames and n-gram
# RETURNS : Files after Prasing and Tokeninzing them.
# NOTE : ngrams is assumed to be 1 for this assignment.
def tokenize_files(filenames):
    file_to_terms = {}
    for file in filenames:
        file_to_terms[file] = [' '.join(x) for x in ngrams(open(file+'.txt', 'r').read().lower(), 1)]
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


# GIVEN : list of Document ID
# Creating an inverted index from the doc to terms hashmap
def get_inverted_index(docid):
    tokens = tokenize_files(docid)
    total = create_index(tokens)
    inverted_index = create_full_index(total)
    return inverted_index

# GIVEN : List of Document ID
# Returns
def get_doc_length(docID):
    doc_len = {}
    for file in docID:
        doc_len[file] = len(open(file+'.txt', 'r').read());
    return doc_len

# Returns a list of queries from queries.txt
def get_queries():
    with open("queries") as f:
        lines = ''.join(f.readlines())
    queries = [x.rstrip().split() for x in lines.split('\n')]
    return queries

#GIVEN : a list of document IDs and document length
#Returns the average document length
def get_avg_doc_len(docid,dlt):
    sum = 0;
    for doc in docid:
        sum = sum + dlt[doc]
    avg = sum / len(dlt)
    return avg

# GIVEN : query, document length, index and average document length
# ranks the documents according to BM25 score.
def rank_terms(query, doc_length, index, avg_dl):
        query_result = {}
        relevant_doc = 0
        query_freq = 1
        for term in query:
            if term in index:
                doc_dict = index[term]
                for docid, freq in doc_dict.items():
                    score = BM25_score(len(doc_dict), freq, query_freq , relevant_doc, len(doc_length)
                                       , len(open(docid + '.txt', 'r').read()), avg_dl)
                    if docid in query_result:
                        query_result[docid] += score
                    else:
                        query_result[docid] = score
        return query_result

def main():

    # Retrieve Document ID from a text file
    doc_id = get_doc_id()
    # Generates a unigram index
    inverted_index = get_inverted_index(doc_id)
    # generates length of document for each doc_id
    doc_length = get_doc_length(doc_id)
    # Retrieves queries from the file queries.txt
    queries = get_queries()
    # Generates the average document length
    avg_doc_length = get_avg_doc_len(doc_id,doc_length)

    # Retrieving the documents in the ranked order
    results = []
    for query in queries:
        results.append(rank_terms(query, doc_length, inverted_index, avg_doc_length))

    qid = 1 # query id

    # Printing the results
    for result in results:
        sorted_x = sorted(result.items(),key=operator.itemgetter(1))
        sorted_x.reverse()
        rank = 1
        for i in sorted_x[:100]:
            print(qid,"\t","Q0","\t",i[0], "\t", rank,"\t",i[1],"\t","VI_BM25")
            rank+=1
        qid +=1

# Program runs from the main function
main()

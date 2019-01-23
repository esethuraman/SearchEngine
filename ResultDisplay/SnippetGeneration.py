from bs4 import BeautifulSoup
from utils.CommonUtils import get_stop_words
import operator
import re
import ntpath

#Snippet window size
WORD_WINDOW_SIZE = 10

#Number of text windows of length WORD_WINDOW_SIZE in the snippet
SNIPPET_LIMIT=3

#Snippets are generated from corpus
INPUT_PLAIN_CORPUS_PATH = "../Files/Input/Corpus/Plain"

def get_snippet(doc_path, qwords):
    print("\n Generating snippets...\n")
    doc_name = ntpath.basename(doc_path).replace(".txt",".html")
    doc_contents = read_doc(INPUT_PLAIN_CORPUS_PATH+"/"+doc_name)
    doc_contents = re.sub(" +"," ",doc_contents)

    #Get all the txt windows from raw docs(original docs)
    text_windows = get_text_windows(doc_contents,WORD_WINDOW_SIZE)

    #highlight text windows based on query words. Stopwords are ignored
    filtered_snippets = filter_snippets(text_windows,SNIPPET_LIMIT,qwords,False)
    snippet = ""

    #If no snippets contain highlighted words, then highlight the stop words
    if len(filtered_snippets) == 0:
        filtered_snippets = filter_snippets(text_windows, SNIPPET_LIMIT, qwords, True)

    #If no words are highlighted, then return the first  SNIPPET_LIMIT text windows
    #This might happen because of words like 'systems,'
    #Notice the comma added to "systems". This hapens for other similar words that contain special chars added
    #to the word without a space.
    if len(filtered_snippets) == 0:
        for x in text_windows[0:SNIPPET_LIMIT]:
            snippet += ' '.join(w for w in x)
        return snippet

    #If only one highlighted snippet is present then return that
    if len(filtered_snippets) > 0 and len(filtered_snippets) == 1 :
        return ' '.join(x for x in text_windows[filtered_snippets[0][0]])

    #Otherwise join all the snippets to make a summary. Summary is seperated by ellipsis ("...")
    #Consecutive snipppet text windows are not delimited by "..."
    #Ex:GEORGE 3-A General Purpose time sharing and operating system An operating system
    # is described which will run on a wide ... same time running several off line (background) jobs. The system ...
    snippet = ""
    if len(filtered_snippets) > 1 :
        for i in range(0,len(filtered_snippets)-1):
            if int(filtered_snippets[i][0])+1 == int(filtered_snippets[i+1][0]):
                snippet += ' '.join(x for x in text_windows[filtered_snippets[i][0]])+" "
            else:
                snippet += ' '.join(x for x in text_windows[filtered_snippets[i][0]])+" ... "

    snippet += ' '.join(x for x in text_windows[filtered_snippets[len(filtered_snippets)-1][0]]) + " ... "
    return snippet

#Read the original html files. Snippets are generated from original files not the cleaned corpus
def read_doc(doc_path):
    with open(doc_path,'r',encoding='utf8') as doc:
        soup = BeautifulSoup(doc.read(), 'html.parser')
        texts = soup.text
        # eliminating the digits at the end of files
        texts = re.sub('\d+\t\d+\t\d+', '', texts)
        return texts.strip()

#Highlight the query words in the text windows and return only the top snippet_limit etxt windows
def filter_snippets(text_windows,snippet_limit,qwords,highlight_stopword):
    stop_words = get_stop_words()
    text_windows_dict = dict()

    #Text windows are weighted by the number of query words present in them
    #larger the weight, the better probability of it making it to the summary
    for qword in qwords:
        if highlight_stopword or qword not in stop_words:
            for i in range(0,len(text_windows)):
                if is_present(qword, text_windows[i]):
                    if i not in text_windows_dict:
                        text_windows_dict[i] = 1
                    else:
                        text_windows_dict[i] += 1

    #Get top SNIPPET_LIMIT snippets where query words are present , Change this to take snippets that have more query words
    sorted_text_windows_dict = sorted(text_windows_dict.items(), key=operator.itemgetter(0))

    #If there are very few windows present, then return all text windows
    if len(sorted_text_windows_dict) <= snippet_limit:
        return list(sorted_text_windows_dict)

    #Otherwise find the best windows (windows where more query wwords are present)
    max=0
    snippet_list = []
    for i in range(0,len(sorted_text_windows_dict)-SNIPPET_LIMIT):
        sum=0
        for j in range(i,i+SNIPPET_LIMIT):
            sum+= sorted_text_windows_dict[j][1]
        if sum > max:
            max = sum
            snippet_list = sorted_text_windows_dict[i:i+SNIPPET_LIMIT]

    return snippet_list

#if the query word is present in the text window, return true
def is_present(qword, text_window):
    for word in text_window:
        if word.lower() == qword.lower():
            return True
    return False

#Split the document into text windows of wthe given window size
def get_text_windows(doc_contents,window_size):
    words = doc_contents.split()
    text_windows = []
    wcount = 0
    wordlist = []

    for word in words:
        if wcount < window_size:
           wordlist.append(word)
           wcount+=1
        else:
            text_windows.append(wordlist)
            wordlist = []
            wordlist.append(word)
            wcount = 1

    #remaining words
    text_windows.append(wordlist)
    return text_windows

#Testing code
#print(get_snippet("E:\\NEU\\Information Retrieval\\Project\\IR\\Files\\Input\\Corpus\\Plain\\CACM-2379.html","what articles exist which deal with tss time sharing system an operating system for ibm computers".split()))
import os

#before calling these methods the corpus should be cleaned
def generate_token_information(cleaned_corpus_path,destination_path):
    tokendict = dict()
    for dir_entry in os.listdir(cleaned_corpus_path):

        dir_entry_path = cleaned_corpus_path+"/"+dir_entry

        # Only if directory entry is a file, won't go through sub directories
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r', encoding="utf8",errors='ignore') as cleaned_file:
                fileContents = cleaned_file.read()
                tokendict[cleaned_file.name] = len(fileContents.split())

    #Write the token information to file
    with open(destination_path,'w',encoding='utf8') as f:
        f.write(str(tokendict))

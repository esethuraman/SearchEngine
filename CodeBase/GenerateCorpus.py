import bs4 as bs
import urllib.request
import re
import time

# GIVEN : SeedURL (string) and Option (int)
# RETURNS : (returns nothing, but) Downloads Corpus with or
#   without Case folding depending on the option chosen.

def bfs_crawl(seed,option):

    depth_list = [seed]
    result_list = []
    depth = 1
    link_pool = []
    relevant_list = []
    count = 0 # to keep track of the limit
    docIdList = set() # TO have a list of unique Document IDs
    bfs_outlinks = {} # Store bfs links
    limit = 1000 # Limit set to 1000 pages

    # Crawling limit set to depth 6
    while (depth <= 6):

        for link in depth_list:

            temp_list = getAllLinksOnPage(link)
            bfs_outlinks[link[30:len(link)]] = temp_list

            time.sleep(1)

            if (link not in result_list):
                result_list.append(link)

            if (len(docIdList) >= limit):
                break;

            for link in temp_list:

                if (link is not 'en.wikipedia.org/wiki/Main_Page' and link not in result_list and link not in link_pool):

                    count = count + 1
                    if(option==1):
                        docIdList.add(link)
                        download_normal_corpus(link)
                    else:
                        docIdList.add(link)
                        download_casefolded_corpus(link)
                    relevant_list.append("https://en.wikipedia.org/wiki/" + link)
                    link_pool.append("https://en.wikipedia.org/wiki/" + link)

                if (count >= limit):

                    for link in depth_list:
                        if (link not in result_list):
                            result_list.append("https://en.wikipedia.org/wiki/" + link)
                    break;

        if (len(docIdList) >= limit):
            break;

        if (count >= limit):
            break;

        depth_list = link_pool

        link_pool = []

        # Stopping at 1000 unique links
        if (len(docIdList) >= limit):
            break;
        depth += 1

    return docIdList

# GIVEN: Seed URL
# RETURNS: All the urls within the seedurl
def getAllLinksOnPage(link):
    temp_links = []
    source_code = urllib.request.urlopen(link).read()

    links_list = re.findall(r'<a href="/wiki/.*?"', str(source_code))
    for link in links_list:
        if ((re.search("[:#]", link)) or (link[15:len(link) - 1]) in 'Main_Page'):
            continue
        else:
            temp_links.append(link[15:len(link) - 1])
    temp_links=list(set(temp_links))
    temp_links1 = []
    for link in temp_links:
        if (link not in temp_links1):
            temp_links1.append(link)

    return temp_links1

# GIVEN : A link to a page
# RETURNS : Downloads A corpus without case folding.
def download_normal_corpus(link):
    source = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + link).read()
    soup = bs.BeautifulSoup(source, "html.parser")
    fo = open(link+'.txt', "w")
    fo.write(soup.title.string + "\n")
    for paragraph in soup.find_all('p'):
        result = paragraph.text
        # Removing displaystyle tag from p tags within file
        var = result.replace("displaystyle", " ")
        fo.write(var.replace("\n", " "))

# GIVEN : A link to a page
# RETURNS : Downloads corpus with casefolding and removing
# punctuation marks
def download_casefolded_corpus(link):
    source = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + link).read()

    soup = bs.BeautifulSoup(source, "html.parser")
    fo = open(link+'.txt', "w")
    regex = r"(?<!\d)[.,;:\{}_^*\\\"\'=()\[\]](?!\d)"
    fo.write(soup.title.string + "\n")
    for paragraph in soup.find_all('p'):
        result = re.sub(regex, "", paragraph.text, 0).lower()
        var = result.replace("displaystyle", " ")
        var2 = var.replace("\n"," ")
        fo.write(var2)

# Main function
def main():
    seed_url = "https://en.wikipedia.org/wiki/Tropical_cyclone"

    option = int(input("Choose one option : \n1.Generate corpus without case folding"
                       "\n2.Generate corpus with case folding\n"))
    print("Downloading Corpus .... ")

    docIdList=bfs_crawl(seed_url,option)

    # Storing all document IDs as a list in
    # DocumentIds.txt
    with open("DocumentIds.txt", "w") as f:
        for s in docIdList:
            f.write(str(s) + "\n")

# calling main function
main()
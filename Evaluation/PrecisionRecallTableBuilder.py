from utils import properties
import operator
# OUTPUT_RELEVANCE_FILE = properties.relevance_info_dict_file
INPUT_RELEVANCE_FILE = properties.relevance_info_file

OUTPUT_PATH = properties.evaluated_scores_output_path

def build_index_for_relevance(INPUT_RELEVANCE_FILE):
    relevance_dict = {}

    with open(INPUT_RELEVANCE_FILE, 'r') as rel_file:
        for line in rel_file:
            line = line.strip()
            if len(line) > 0:
                line_contents = line.split()

                # first string contains the query id
                # third string contains the document id
                q_id = line_contents[0]
                doc_id = line_contents[2]

                # TODO - format docids so that this part is ignored
                if doc_id.endswith('.txt'):
                    doc_id_contents = doc_id.split('/')
                    doc_id = doc_id_contents[len(doc_id_contents)-1]
                    doc_id = doc_id[:-4]


                if q_id not in relevance_dict:
                    relevance_dict[q_id] = [doc_id]
                else:
                    doc_lst = relevance_dict[q_id]

                    doc_lst.append(doc_id)
                    relevance_dict[q_id] = doc_lst
    return relevance_dict

# precision and recall values are truncated to 4 decimal points
def truncate_if_long(float_value):
    return "{0:.4f}".format(float_value)

# space formatting rank values for better output visualization
def format_space(rank_value):
    no_of_digits =  len(str(rank_value))
    rank_as_string = str(rank_value)

    if no_of_digits == 1:
        rank_as_string += "  "
    elif no_of_digits == 2:
        rank_as_string += " "
    return rank_as_string

def write_in_to_file(precision_recall_dict, SYSTEM_NAME):
    sorted_precision = sorted(precision_recall_dict.items(),key=operator.itemgetter(0))
    with open(OUTPUT_PATH + "/PrecisionRecall"+SYSTEM_NAME + ".csv", 'w') as file:
        file.write(60*"-" + "\n")
        file.write("QueryID,RANK,DOC_ID,PRECISION,RECALL\n")
        file.write(60 * "-" + "\n")
        for q_id, rank_scores_dict in sorted_precision:

            # file.write(q_id + "  " + str(rank_scores_dict) + "\n")
            for i in range(len(rank_scores_dict.keys())):
                file.write(q_id + ",")
                rank = i+1
                doc_prec_recall_lst = rank_scores_dict[i+1]
                file.write(str(format_space(rank)) + "," +
                           str(doc_prec_recall_lst[0]) + "," +
                           str(truncate_if_long(doc_prec_recall_lst[1])) + "," +
                           str(truncate_if_long(doc_prec_recall_lst[2])) + "\n")


            file.write("\n")

def get_precision_recall_table(INPUT_SCORES_FILE, SYSTEM_NAME):
    # getting dictionaries
    relevance_info_dict = build_index_for_relevance(INPUT_RELEVANCE_FILE)
    scores_info_dict = build_index_for_relevance(INPUT_SCORES_FILE)

    # {q_id : {rank : [doc_id, precision, recall] } }
    precision_recall_dict = {}

    for q_id, relevance_docs_lst in relevance_info_dict.items():

        visited_relevance_docs_count = 0
        precision_recall_dict[q_id] = {}

        ranked_docs_lst = scores_info_dict[q_id]
        count_relevance_docs = len(relevance_docs_lst)

        for i in range(len(ranked_docs_lst)):
            # the docs are already ranked. so i value is the rank
            rank = i + 1
            doc_id = ranked_docs_lst[i]
            precision_recall_dict[q_id][rank] = []

            # if the found document is a relevant document
            if ranked_docs_lst[i] in relevance_docs_lst:
                visited_relevance_docs_count += 1

            # calculating precision and recall
            precision = visited_relevance_docs_count / rank
            recall = visited_relevance_docs_count / count_relevance_docs

            # storing the computed values
            precision_recall_dict[q_id][rank] = [doc_id, precision, recall]
    write_in_to_file(precision_recall_dict, SYSTEM_NAME)

    return precision_recall_dict


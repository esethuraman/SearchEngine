from Evaluation.PrecisionRecallTableBuilder import get_precision_recall_table
from utils import properties
import operator

def get_MAP_value(precision_recall_dict):
    avg_precision_lst = []

    for q_id, docs_dict in precision_recall_dict.items():
        prev_precision_numerator = 0

        total_precision = 0
        no_of_relevant_docs = 0

        for rank, doc_prec_recall_lst in docs_dict.items():
            current_precision = doc_prec_recall_lst[1]
            if not (current_precision == (prev_precision_numerator/rank)):
                total_precision += current_precision
                no_of_relevant_docs += 1

            prev_precision_numerator = current_precision * rank
        if no_of_relevant_docs == 0:
            avg_precision_lst.append(0)
        else:
            avg_precision_lst.append(total_precision/no_of_relevant_docs)

    mean_avg_precision = (sum(avg_precision_lst)) / len(avg_precision_lst)
    return mean_avg_precision

def get_MRR_value(precision_recall_dict):
    reciprocal_rank_lst = []
    for q_id, docs_dict in precision_recall_dict.items():
        for rank, doc_prec_call_lst in docs_dict.items():
            precision = doc_prec_call_lst[1]
            if (precision > 0):
                reciprocal_rank_lst.append(1/rank)
                break
    mean_reciprocal_rank = (sum(reciprocal_rank_lst))/ (len(reciprocal_rank_lst))
    return mean_reciprocal_rank

def get_PR_at_K(precision_recall_dict, K):
    prAtK_dict = dict()
    for q_id, docs_dict in precision_recall_dict.items():
        prAtK_dict[q_id] = docs_dict[K][1]
    return prAtK_dict


def find_effectiveness_scores(INPUT_SCORES_FILE, SYSTEM_NAME):
    # [MAP_Score, MRR_Score, {PR@5 Score dict}, {PR@20 Score dict}]
    all_results_list = []
    precision_recall_dict = get_precision_recall_table(INPUT_SCORES_FILE,SYSTEM_NAME)

    MAP_score = get_MAP_value(precision_recall_dict)

    MRR_score = get_MRR_value(precision_recall_dict)

    prAt5_dict = get_PR_at_K(precision_recall_dict, 5)
    prAt20_dict = get_PR_at_K(precision_recall_dict, 20)

    all_results_list = [MAP_score, MRR_score, prAt5_dict, prAt20_dict]
    write_results_to_file(all_results_list, SYSTEM_NAME)

def write_results_to_file(all_results_list, SYSTEM_NAME):

    output_file_name = properties.evaluated_scores_output_path+"/EvaluationResults_"+SYSTEM_NAME+".csv"

    prAt5_dict = all_results_list[2]
    sorted_prAt5 = sorted(prAt5_dict.items(),key=operator.itemgetter(0))

    prAt20_dict = all_results_list[3]
    sorted_prAt20 = sorted(prAt20_dict.items(),key=operator.itemgetter(0))


    with open(output_file_name, 'w') as file:
        file.write("\n" + 60 * "-"+"\n")
        file.write("MEAN AVERAGE PRECISION   : " +  str(all_results_list[0]) + "\n")
        file.write("\n")
        file.write("\n")
        file.write("MEAN RECIPROCAL RANK     : " +  str(all_results_list[1]) + "\n")
        file.write("\n")

        file.write("\n")
        file.write("PR@5 :" + "\n")
        file.write("\n")
        file.write("QueryID,Precision Score\n")
        for q_id, pr_score in sorted_prAt5:
            file.write(str(q_id) + "," + str(pr_score) + "\n")

        file.write("\n")
        file.write("PR@20 :" + "\n")
        file.write("\n")
        file.write("QueryID,Precision Score\n")
        for q_id, pr_score in sorted_prAt20:
            file.write(str(q_id) + "," + str(pr_score) + "\n")

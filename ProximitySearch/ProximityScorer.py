import operator

def get_proximity_scored_dict(docs_pos_dict):

    docs_scores_dict = {}

    for doc_id, pos_list in docs_pos_dict.items():
        cumulative_score = 0

        if len(pos_list) == 1:
            cumulative_score = 1

        else:
            is_eligible = True
            is_begining_list = True
            begining_list = pos_list[0]
            vistied_count_begining_list = 0
            lookup_position = None

            i = 0
            while (i != (len(pos_list)-1)):
                first_lst = pos_list[i]
                second_lst = pos_list[i+1]

                if lookup_position == None:
                    lookup_position = first_lst[i]


                for j in range (first_lst.index(lookup_position), len(first_lst)):
                    if is_begining_list:
                        # the cumulative score has to be reset now
                        cumulative_score = 0
                        lookup_position = begining_list[vistied_count_begining_list]
                        vistied_count_begining_list += 1

                    if (lookup_position + 1) in second_lst:
                        lookup_position = lookup_position + 1
                        cumulative_score += 1
                        is_begining_list = False
                        i += 1
                        break
                    elif (lookup_position + 2) in second_lst:
                        lookup_position = lookup_position + 2
                        cumulative_score += 2
                        is_begining_list = False
                        i += 1
                        break
                        # break
                    elif (lookup_position + 3) in second_lst:
                        lookup_position = lookup_position + 3
                        cumulative_score += 3
                        is_begining_list = False
                        i += 1
                        break
                        # break
                    elif (j == (len(first_lst)-1)):
                        if (vistied_count_begining_list == len(begining_list)):
                            is_eligible = False
                            # break
                        else:
                            # reiterating the loop from the begining but with the lookup term in that begining
                            # list moved to the next window (of size 1)
                            i = 0
                            lookup_position = begining_list[vistied_count_begining_list]
                            is_begining_list = True
                            break

                    else:
                        continue

                if not is_eligible:
                    break
            # print(is_eligible)

        # dividing cumulative score by 1 to keep it proportional to rank
        if not (cumulative_score == 0) :
            cumulative_score = 1/cumulative_score

        # writing scores to dictionary
        if (not (cumulative_score == 0)) and (is_eligible):
            docs_scores_dict[doc_id] = cumulative_score
        # print(is_eligible)
        # print("SCORE ", cumulative_score)
    sorted_tuple = sorted(docs_scores_dict.items(), key=operator.itemgetter(1))
    # print("SCORED DOCS ", dict(sorted_tuple) ,"\n")
    print("[INFO] Exact matches search completed...")
    return(dict(sorted_tuple))

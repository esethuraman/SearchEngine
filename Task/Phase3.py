# This program outputs Evaluation results on the four Retreival systems,
# on the normal corpus and stopped corpus

from Evaluation.EffectivenessFinder import find_effectiveness_scores
# find_effectiveness_scores("../Files/Output/Ranking/BM25_CASEFOLD_1GRAM.txt", "BM25")

BM25_RANKING_RESULT = "../Files/Output/Ranking/BM25_CASEFOLD_1GRAM.txt"
BM25_STOP_RANKING_RESULT = "../Files/Output/Ranking/BM25_STOP_CASEFOLD_1GRAM.txt"
BM25_PRF_RANKING_RESULT = "../Files/Output/Ranking/BM25_CASEFOLD_PRF_1GRAM_k7_n2.txt"
TFIDF_RANKING_RESULT = "../Files/Output/Ranking/TFIDF_CASEFOLD_1GRAM.txt"
TFIDF_STOP_RANKING_RESULT = "../Files/Output/Ranking/TFIDF_STOP_CASEFOLD_1GRAM.txt"
QLM_RANKING_RESULT = "../Files/Output/Ranking/QLM_CASEFOLD_1GRAM.txt"
QLM_STOP_RANKING_RESULT = "../Files/Output/Ranking/QLM_STOP_CASEFOLD_1GRAM.txt"

def main():
    # Finding effectiveness scores on BM25 model on a normal corpus
    find_effectiveness_scores(BM25_RANKING_RESULT, "BM25_CASEFOLD_1GRAM")

    # Finding effectiveness scores on BM25 model on stopped corpus
    find_effectiveness_scores(BM25_STOP_RANKING_RESULT, "BM25_STOP_CASEFOLD_1GRAM")

    # Finding effectiveness scores on BM25 rankings obtained on Pseudo Relevance feedback
    find_effectiveness_scores(BM25_PRF_RANKING_RESULT,"BM25_CASEFOLD_PRF_1GRAM_k7_n2")

    # Finding effectiveness scores on TFIDF model on a normal corpus
    find_effectiveness_scores(TFIDF_RANKING_RESULT, "TFIDF_CASEFOLD_1GRAM")

    # Finding effectiveness scores on TFIDF model on stopped corpus
    find_effectiveness_scores(TFIDF_STOP_RANKING_RESULT, "TFIDF_STOP_CASEFOLD_1GRAM")

    # Finding effectiveness scores on QLM model on a normal corpus
    find_effectiveness_scores(QLM_RANKING_RESULT, "QLM_CASEFOLD_1GRAM")

    # Finding effectiveness scores on QLM model on stopped corpus
    find_effectiveness_scores(QLM_STOP_RANKING_RESULT, "QLM_STOP_CASEFOLD_1GRAM")


if __name__ == '__main__':
    main()




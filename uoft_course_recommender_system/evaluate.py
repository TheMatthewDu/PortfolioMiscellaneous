import numpy as np
import joblib

from scipy.sparse import load_npz
from sklearn.naive_bayes import MultinomialNB


def main():
    name_list = open("data/uoft_labels.csv").read().split(sep="\n")
    desc = load_npz("data/all_descriptions.npz").toarray()

    course_name = input("Course code: ")
    k = name_list.index(list(filter(lambda x: course_name in x, name_list))[0])

    model: MultinomialNB = joblib.load("model.sav")
    log_prob = model.feature_log_prob_

    probabilities = np.matmul(log_prob, desc[k])
    for _ in range(20):
        highest_index = np.argmax(probabilities)
        print(name_list[highest_index])
        probabilities[highest_index] = min(probabilities)


if __name__ == "__main__":
    main()

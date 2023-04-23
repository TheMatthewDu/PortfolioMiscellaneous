import tqdm
import numpy as np
import scipy as sp
import joblib

from scipy.sparse import load_npz
from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import MultinomialNB

NUM_CLASSES = 537
NUM_FEATURES = 5024


def main():
    all_data: sp.sparse.csr_matrix = load_npz("data/training_data.npz")
    all_targets = np.load("data/training_targets.npy")

    train_data, test_data, train_targets, test_targets = train_test_split(all_data, all_targets, train_size=0.7, test_size=0.3)

    train_data = train_data.toarray()
    test_data = test_data.toarray()

    print("Data Has Been Loaded")
    model = MultinomialNB()
    model.fit(train_data, train_targets)

    print("Data Has Been Fitted")
    train_results = model.predict(train_data)
    test_results = model.predict(test_data)

    # Evaluation
    print("Train Accuracy", np.count_nonzero(train_results == train_targets) / len(train_results))
    print("Test Accuracy", np.count_nonzero(test_results == test_targets) / len(test_results))

    joblib.dump(model, "model.sav")


if __name__ == "__main__":
    main()

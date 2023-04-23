import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from scipy.sparse import save_npz


def main():
    data: pd.DataFrame = pd.read_csv("data/uoft_clean.csv")

    frequency_table: pd.Series = data["Description"].str.split(expand=True).stack().value_counts()
    list_of_descriptions: list[str] = data["Description"].tolist()

    training_data_phrases, training_targets = get_data(list_of_descriptions, frequency_table)

    vectorizer = CountVectorizer()

    all_descriptions = vectorizer.fit_transform(list_of_descriptions)
    training_data = vectorizer.transform(training_data_phrases)

    print(all_descriptions.shape, training_data.shape)
    save_npz("data/training_data.npz", training_data)
    save_npz("data/all_descriptions.npz", all_descriptions)
    np.save("data/training_targets.npy", np.array(training_targets))


def get_data(desc_list, frequency_table):
    x, y = [], []
    for i, desc in enumerate(desc_list):
        # Remove infrequent words
        frequent_word_list = np.array(
            [word for word in desc.split(sep=' ') if word in frequency_table and frequency_table[word] < 100]
        )

        for sample in range(50):
            mask = np.random.randint(0, 2, len(frequent_word_list), dtype=bool)
            x.append(" ".join(frequent_word_list[mask]))
            y.append(i)
    return x, y


if __name__ == "__main__":
    main()

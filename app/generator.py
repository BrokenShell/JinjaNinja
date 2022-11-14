from Fortuna import random_value, percent_true

import pandas

from app.sentiment import sentiment_rank


class RandomInput:
    corpus = pandas.read_csv("app/data/corpus.csv")["text"]
    last_names = pandas.read_csv("app/data/last-names.csv")["last_name"]
    female_names = pandas.read_csv("app/data/female-names.csv")["first_name"]
    male_names = pandas.read_csv("app/data/male-names.csv")["first_name"]

    def __init__(self):
        self.Name = f"{self.random_first(60)} {random_value(self.last_names)}"
        self.Text = random_value(self.corpus)
        self.Sentiment = sentiment_rank(self.Text)

    def random_first(self, percent_female):
        if percent_true(percent_female):
            return random_value(self.female_names)
        else:
            return random_value(self.male_names)

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())


if __name__ == '__main__':
    print(RandomInput())

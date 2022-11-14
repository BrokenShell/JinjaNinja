import pandas
from flask import Flask, render_template, request

from app.database import MongoDB
from app.sentiment import sentiment_rank

APP = Flask(__name__)
DB = MongoDB()


@APP.route("/")
@APP.route("/home")
def home_page():
    return render_template("home.html")


@APP.route("/output")
def output_page():
    count = DB.count()
    if count > 0:
        table = DB.html_table()
    else:
        table = "<p>No data yet!</p>"
    return render_template("output.html", count=count, table=table)


@APP.route("/input", methods=["GET", "POST"])
def input_page():
    if request.method == "POST":
        name = request.values.get("name")
        text = request.values.get("text", "")
        if name == "/clear":
            DB.reset()
            return output_page()
        elif name == "/seed":
            DB.seed(int(text or 100))
            return output_page()
        else:
            DB.create({
                "Name": name,
                "Text": text,
                "Sentiment": sentiment_rank(text),
            })
            return output_page()
    return render_template("input.html")


@APP.route("/seed", methods=["GET", "POST"])
def seed_page():
    if request.method == "POST":
        amount = request.values.get("amount", type=int)
        target_sentiment = request.values.get("sentiment")
        df = pandas.read_csv("app/data/corpus.csv")
        df = df[df["text"].apply(
            lambda x: sentiment_rank(x) == target_sentiment
        )]
        df["sentiment"] = target_sentiment
        table = df.sample(amount, replace=True).to_html()
        return render_template("seed.html", table=table)
    return render_template("seed.html")


if __name__ == '__main__':
    APP.run()

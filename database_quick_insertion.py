from models import db, MyComment
import spacy
from flask import Flask
import valuation


app = Flask(__name__)
app.secret_key = "jfnr83$#2jf@D8sajdklh1208dfh!"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

nlp = spacy.load("pt_core_news_lg")

with open("valuation/topics.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
dicts = [eval(line.strip()) for line in lines]

with app.app_context():
    comments = MyComment.query.all()
    for comment in comments:
        # comment.embedding = nlp(comment.content).vector.tolist()
        if comment.product_id == 1:
            nouns = dicts[0]
            comment.value = valuation.valuate_opinion(comment.content, nlp, nouns)
        elif comment.product_id == 2:
            nouns = dicts[1]
            comment.value = valuation.valuate_opinion(comment.content, nlp, nouns)
        elif comment.product_id == 3:
            nouns = dicts[2]
            comment.value = valuation.valuate_opinion(comment.content, nlp, nouns)
    db.session.commit()

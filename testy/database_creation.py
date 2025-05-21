import random
from datetime import datetime, timedelta
from app import create_app, db
from models import MyComment, MyProduct, User
from sentiment import load_saved_model, predict_comment
from valuation import valuate_opinion
import spacy

from testy.tests_comment_lists import telephone_pt, robot_pt, watch_pt  # zamień na bezpośredni import lub wklej

nlp = spacy.load("pt_core_news_lg")
tokenizer, model = load_saved_model()

with open("valuation/topics.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
dicts = [eval(line.strip()) for line in lines]

def random_date_this_year():
    start = datetime(2025, 1, 1)
    end = datetime(2025, 2, 28)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

DATA = [
    ("telefone", telephone_pt, dicts[0]),
    ("robô", robot_pt, dicts[1]),
    ("assistir", watch_pt, dicts[2])
]

app = create_app()

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

    for name, comments, nouns in DATA:
        product = MyProduct.query.filter_by(product_name=name).first()
        if not product:
            product = MyProduct(product_name=name, admin_name=admin.username)
            db.session.add(product)
            db.session.commit()

        for content in comments:
            sentiment = predict_comment(model, tokenizer, "cpu", content)
            value = valuate_opinion(content, nlp, nouns)

            new_comment = MyComment(
                product_id=product.product_id,
                user=str(random.randint(1, 1000)),
                content=content,
                result=sentiment,
                value=value,
                created_on=random_date_this_year()
            )
            db.session.add(new_comment)

    db.session.commit()
    print("✅ Produkty i komentarze dodane do bazy danych.")

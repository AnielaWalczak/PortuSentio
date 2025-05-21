from flask import Flask, request, render_template, redirect, jsonify, send_file, flash
from sentiment import load_saved_model, predict_comment
from valuation import valuate_opinion, valuate_opinion_for_custom_product
from flask_login import LoginManager, login_required, current_user
from datetime import datetime
import spacy

from models import db, User, MyComment, MyProduct
from auth import auth
from report_pdf import generate_pdf

nlp = spacy.load("pt_core_news_lg")
tokenizer, model = load_saved_model()

with open("valuation/topics.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
dicts = [eval(line.strip()) for line in lines]


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = "jfnr83$#2jf@D8sajdklh1208dfh!"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        products = MyProduct.query.all()
        if request.method == 'POST':
            content = request.form['content']
            selected_product_id = int(request.form['product_id'])
            sentiment = predict_comment(model, tokenizer, 'cpu', content)
            if selected_product_id in [1, 2, 3]:
                nouns = dicts[selected_product_id - 1]
                value = valuate_opinion(content, nlp, nouns)
            else:
                value = valuate_opinion_for_custom_product(content, nlp)

            if current_user.is_authenticated:
                user = current_user.username
            else:
                user = "anônimo"

            embedding = nlp(content).vector.tolist()

            new_comment = MyComment(
                product_id=selected_product_id,
                user=user,
                content=content,
                result=sentiment,
                value=value,
                embedding=embedding
            )

            db.session.add(new_comment)
            db.session.commit()
            return redirect("/sucesso")
        return render_template('index.html', products=products)

    @app.route('/predict', methods=['POST'])
    def predict():
        data = request.json
        comment = data.get("content", "")
        if not comment.strip():
            return jsonify({"error": "Comentário não pode estar vazio"}), 400
        sentiment = predict_comment(model, tokenizer, 'cpu', comment)
        emoji = {"positivo": "😊", "negativo": "😞"}.get(sentiment.lower(), "😐")
        return jsonify({"sentiment": emoji})

    @app.route('/valuate', methods=['POST'])
    def valuate():
        data = request.json
        content = data.get("content", "")
        product_id = data.get("product_id")
        if not content.strip():
            return jsonify({"error": "Comentário não pode estar vazio"}), 400
        if not product_id:
            return jsonify({"error": "Produto não selecionado"}), 400
        try:
            product_index = int(product_id) - 1
            if product_index in [0, 1, 2]:
                nouns = dicts[product_index]
                value = valuate_opinion(content, nlp, nouns)
            else:
                value = valuate_opinion_for_custom_product(content, nlp)

            return jsonify({"value": value})
        except Exception:
            return jsonify({"error": "Erro interno"}), 500

    @app.route('/check-comments')
    def check_comments():
        product_id = request.args.get('product', type=int)
        date_from_str = request.args.get('from')
        date_to_str = request.args.get('to')
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d')
        except Exception:
            return jsonify({'error': 'Invalid date format'}), 400
        count = MyComment.query.filter(
            MyComment.product_id == product_id,
            MyComment.created_on >= date_from,
            MyComment.created_on <= date_to
        ).count()
        return jsonify({'count': count})

    @app.route('/revisão', methods=['GET', 'POST'])
    def index2():
        comments = MyComment.query.order_by(MyComment.created_on.desc()).all()
        return render_template('revisão.html', comments=comments)

    @app.route('/relatório', methods=['GET', 'POST'])
    @login_required
    def index3():
        if not current_user.is_admin:
            return redirect("/")
        products = MyProduct.query.all()
        if request.method == 'POST':
            product_id = int(request.form['product_id'])
            product = MyProduct.query.get(product_id)
            date_from = datetime.strptime(request.form['date_from'], '%Y-%m-%d')
            date_to = datetime.strptime(request.form['date_to'], '%Y-%m-%d')

            if (date_to - date_from).days < 30:
                flash('Zakres dat musi wynosić co najmniej 30 dni.', 'error')
                return redirect(request.url)

            comments = MyComment.query.filter(
                MyComment.product_id == product_id,
                MyComment.created_on >= date_from,
                MyComment.created_on <= date_to
            ).all()

            if len(comments) < 30:
                flash('Não há comentários suficientes (mínimo: 30) no período selecionado.', 'error')
                return redirect(request.url)

            pdf_buffer = generate_pdf(product.product_name, date_from, date_to, comments)
            pdf_buffer.seek(0)
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                download_name=f"{product.product_name}_relatório_{date_from.strftime('%d-%m-%Y')}_até_"
                              f"{date_to.strftime('%d-%m-%Y')}.pdf"
            )
        return render_template('relatório.html', products=products)

    @app.route('/sucesso', methods=['GET', 'POST'])
    def index4():
        return render_template('sucesso.html')

    @app.route("/add_produto", methods=['GET', 'POST'])
    @login_required
    def manage_products():
        if not current_user.is_admin:
            return redirect("/")
        products = MyProduct.query.filter_by(admin_name=current_user.username).all()
        if request.method == "POST":
            try:
                product_data = request.get_json()
                product_name = product_data.get("product_name")
                if not product_name:
                    return jsonify({"error": "O nome do produto é obrigatório"}), 400
                new_product = MyProduct(product_name=product_name, admin_name=current_user.username, active=True)
                db.session.add(new_product)
                db.session.commit()
                return jsonify({"success": "Produto adicionado com sucesso!"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return render_template("product.html", products=products)

    @app.route('/toggle_ativo/<int:product_id>', methods=['GET', 'POST'])
    @login_required
    def toggle_ativo(product_id):
        product = MyProduct.query.filter_by(product_id=product_id, admin_name=current_user.username).first()
        if not product:
            return jsonify({'success': False, 'error': 'Produto não encontrado'}), 404
        try:
            product.active = not product.active
            db.session.commit()
            return jsonify({'success': True, 'active': product.active})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    return app

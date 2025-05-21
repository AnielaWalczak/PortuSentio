from flask import Blueprint, jsonify, request, render_template, redirect
from flask_login import login_user, login_required, logout_user
from models import db, User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    error = None
    success_message = None
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            success_message = "Login realizado com sucesso!"
            return render_template("login.html", success_message=success_message)
        else:
            error = "Detalhes de login incorretos"

    return render_template("login.html", error = error)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@auth.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success_message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]

        if password != password2:
            error = "As senhas não são as mesmas"
        elif User.query.filter_by(username=username).first():
            error = "O usuário com esse login já existe"
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            success_message = "Cadastro realizado com sucesso! Você pode fazer login agora."
            return render_template("register.html", success_message=success_message)

    return render_template("register.html", error=error)


@auth.route("/check_username", methods=["POST"])
def check_username():
    data = request.get_json()
    username = data.get("username")
    
    if User.query.filter_by(username=username).first():
        return jsonify({"available": False}) 
    else:
        return jsonify({"available": True})

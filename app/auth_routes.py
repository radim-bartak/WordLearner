from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/")
def index():
    return render_template("index.html")

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            return "Uživatel již existuje!"
        pw_hash = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username, password_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth_bp.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("main_bp.choose_theme"))
        else:
            return "Neplatné přihlašovací údaje"
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth_bp.index"))

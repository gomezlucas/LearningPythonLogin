from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from .models import User
from flask_login import login_user, logout_user, login_required
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user and not password == user.password:
        flash("please check your login message and try again")
        return redirect(url_for("auth.login"))
    print(f"a veeeerrr {user}")
    login_user(user, remember = remember)
   
    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address already exists")
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

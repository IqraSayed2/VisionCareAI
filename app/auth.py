from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/auth", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action")

        # ---------- LOGIN ----------
        if action == "login":
            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("main.detect"))
            else:
                flash("Invalid email or password", "danger")

        # ---------- SIGNUP ----------
        if action == "signup":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirm")

            if password != confirm:
                flash("Passwords do not match", "danger")
                return redirect(url_for("auth.login"))

            if User.query.filter_by(email=email).first():
                flash("Email already exists", "danger")
                return redirect(url_for("auth.login"))

            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for("main.detect"))

    return render_template("auth.html")


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))

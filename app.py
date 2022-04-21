from flask import Flask, render_template, request, flash, url_for, redirect
import random
from sqlalchemy.orm import sessionmaker
from DowlaondData import createlistQustion
from UserForm import UserRegister, UserLogin
from UserModel import User, engine
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_bootstrap import Bootstrap
from Translation import translation
from usunprefiks import usunprefiks

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "Tajny klucz"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
Bootstrap(app)


@login_manager.user_loader
def load_user(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(User).filter_by(id=int(user_id)).one()


data = createlistQustion()



@login_required
@app.route("/", methods=["GET", "POST"])
def index():
    i = random.choice(data)
    question = "Wylosuj jeszcze raz"
    answer = "Wylosuj jeszcze raz"
    if i.getQuestion() != None and i.getAnswer() != None:
        question = usunprefiks(translation(i.getQuestion()))
        answer = usunprefiks(translation(i.getAnswer()))
    if request.method == "POST":
        current_user.setnumber_of_points(50)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.query(User).filter_by(user_name=current_user.getName()).update(
            {"number_of_points": current_user.getnumber_of_points()}
        )
        session.commit()
        session.close()
    return render_template("index.html", question=question, answer=answer)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = UserRegister()
    if request.method == "POST" and form.validate():
        # pobranie danych z formularza
        nameuser = request.form["name_user"]
        password = request.form["password"]
        e_mail = request.form["e_mail"]
        # połączenie z bazą danych
        Session = sessionmaker(bind=engine)
        session = Session()
        # stworzenie nowego uzytkownika
        user = User()
        user.user_name = nameuser
        user.password = password
        user.e_mail = e_mail
        user.number_of_points = 100
        # zapis użytkownika do bazy danych
        session.add(user)
        session.commit()
        session.close()
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = UserLogin()
    Session = sessionmaker(bind=engine)
    session = Session()
    if request.method == "POST" and form.validate():
        user = session.query(User).filter_by(user_name=request.form["name_user"]).one()
        if user.getPassword() == request.form["password"]:
            login_user(user)
            flash("Logged in successfully.")
            inf = "Zostałeść zalogowany"
            return render_template("login.html", form=form, inf=inf)
        else:
            inf = "Podałeść błędne dane"
            return render_template("login.html", form=form, inf=inf)
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
# set FLASK_ENV=development

from flask import Flask, render_template, request
import random
from sqlalchemy.orm import sessionmaker
from DowlaondData import dowlaondData
from UserForm import UserRegister, UserLogin
from UserModel import User, engine

app=Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'Tajny klucz'

@app.route('/')
def index():
    # Dane
    data = dowlaondData()
    # Losowanie pytania
    i = random.choice(data)
    question = i.getQuestion()
    answer = i.getAnswer()

    return render_template("index.html", question=question, answer=answer)

@app.route('/registration', methods=['GET', 'POST'])
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

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UserLogin()
    Session = sessionmaker(bind=engine)
    session = Session()
    if request.method == "POST" and form.validate():
        user = session.query(User).filter_by(user_name=request.form["name_user"]).one()
        if user.getPassword() == request.form['password']:
            inf = "Zostałeść zalogowany"
            return render_template("login.html", form=form, inf=inf)
        else:
            inf = "Podałeść błędne dane"
            return render_template("login.html", form=form, inf=inf)
        return render_template("login.html", form=form, inf=inf)
    return render_template("login.html", form=form)
if __name__=="__main__":
    app.run()

import hashlib
import re
import numpy as np

from flask import Flask, render_template, redirect, request, url_for, session, flash

from data_utils import get_rand_number, get_numbers_list
from databases_utils import elastic_database

database = elastic_database()

app = Flask(__name__)
app.secret_key = "ayush"


@app.route('/')
def home():
    if 'email' in session:
        email = session['email']
        return render_template('Web_ini_logged.html', user=email)
    else:
        n = get_rand_number()
        data = {
            "number": n
        }
        database.post_info("random_num", data)
        return render_template('Web_ini.html', num=n)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/user', methods=["POST"])
def check_user():
    if request.method == "POST":
        email = request.form['email']
        passw = request.form['pass']
        email_search = database.get_info("user_data", q = {"match_phrase": {"email": email}})
        
        if len(email_search['hits']['hits']) == 0:
            return "Email no registrado"
        else:
            data = email_search['hits']['hits']
            if passw == data[0]['_source']['pass']:
                session['email'] = email
                return render_template('login_success.html')
            else:
                return "Password incorrecta"

@app.route('/new_user', methods=["POST"])
def new_user():
    if request.method == "POST":
        new_user = request.form['username']
        new_mail = request.form['email']
        new_pass = request.form['pass']

        user_search = database.get_info("user_data", q = {"match_phrase": {"username": new_user}})
        email_search = database.get_info("user_data", q = {"match_phrase": {"email": new_mail}})

        if len(user_search['hits']['hits']) == 0 and len(email_search['hits']['hits']) == 0:
            data = {
                "username": new_user,
                "email": new_mail,
                "pass": new_pass
            }
            database.post_info("user_data", data)
            session['email'] = new_mail
            return render_template('login_success.html')
        else:
            return "Usuario o email ya registrado"

@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
        return render_template('logout.html')

@app.route('/profile')
def profile():
    if 'email' in session:
        email = session['email']
        return render_template('profile.html', name=email)


@app.route('/local_mean')
def local_mean():
    data = database.get_info("random_num")
    mean = np.mean(get_numbers_list(data['hits']['hits']))
    print(get_numbers_list(data['hits']['hits']))
    return render_template('mean.html', bbdd='local', num=mean)

@app.route('/cloud_mean')
def cloud_mean():
    return 

if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)

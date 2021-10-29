import hashlib
import re
import numpy as np
import argparse

from flask import Flask, render_template, redirect, request, url_for, session, flash

from data_utils import get_rand_number, get_numbers_list, get_cloud_numbers_list
from databases_utils import elastic_database, beebote_database, reset_database

database = elastic_database()
cloud_database = beebote_database()

app = Flask(__name__)
app.secret_key = "ayush"


@app.route('/')
def home():

    ## Comprobamos si hay sesion iniciada para mostrar la Web

    if 'email' in session:

        # Si hay user se muestran mas opciones y sus datos (email y accesos a medias)

        email = session['email']
        user_info = database.get_info("user_data", q = {"match_phrase": {"email": email}})[0]

        return render_template('Web_ini_logged.html', user=user_info['_source']['username'],\
             local_n = user_info['_source']['n_local_acc'], cloud_n = user_info['_source']['n_cloud_acc'])

    else:

        # Si no hay sesion iniciada se extrae un numero y se muestra y almacena en las BBDD

        n = get_rand_number()
        data = {
            "number": n
        }
        database.post_info("random_num", data)
        cloud_database.post_info("Cer_p1","random_n",data=n)

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
        
        if len(email_search) == 0:
            return "Email no registrado"
        elif len(email_search) > 1:
            return "Error en la cuenta, contacte con el admin de la app"
        else:
            data = email_search
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

        if len(user_search) == 0 and len(email_search) == 0:
            data = {
                "username": new_user,
                "email": new_mail,
                "pass": new_pass,
                "n_local_acc": 0,
                "n_cloud_acc": 0
            }
            
            database.post_info("user_data", data)

            # Guardamos una copia de los user data en la nube

            data = {
                "username": new_user,
                "email": new_mail,
                "pass": new_pass,
            }
            cloud_database.post_info("Cer_p1","user_data",data)

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
    if 'email' in session:
        ## Obtenemos la media de todos los num
        data = database.get_info("random_num")
        mean = np.mean(get_numbers_list(data))
        print(get_numbers_list(data))

        ## Buscamos los datos del usuario para actualizar las veces que ha solicitado la media y lo guardamos en la BBDD
        user_data = database.get_info("user_data", q = {"match_phrase": {"email": session['email']}})[0]
        user_data['_source']['n_local_acc'] += 1
        database.post_info(index_name="user_data",_id = user_data['_id'],doc=user_data['_source'])

        return render_template('mean.html', bbdd='local', num=mean)
    else:
        return "Usuario no identificado, inicie sesion"

@app.route('/cloud_mean')
def cloud_mean():
    if 'email' in session:
        data = cloud_database.get_info("Cer_p1","random_n")
        mean = np.mean(get_cloud_numbers_list(data))
        print(get_cloud_numbers_list(data))        

        ## Buscamos los datos del usuario para actualizar las veces que ha solicitado la media y lo guardamos en la BBDD
        user_data = database.get_info("user_data", q = {"match_phrase": {"email": session['email']}})[0]
        user_data['_source']['n_cloud_acc'] += 1
        database.post_info(index_name="user_data",_id = user_data['_id'],doc=user_data['_source'])

        return render_template('mean.html', bbdd='cloud', num=mean)

    else:
        return "Usuario no identificado, inicie sesion"

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html')
    else:
        return "Usuario no identificado, inicie sesion"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-reset", "--res_database",
                        help="Eliminar datos de los indices de numeros y users", action="store_true")
    args = parser.parse_args()
    
    if args.res_database:

        reset_database()
    
    # app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)

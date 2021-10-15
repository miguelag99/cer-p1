from flask import Flask, render_template, redirect, request, url_for, session, flash

from data_utils import get_rand_number


app = Flask(__name__)  
app.secret_key = "ayush"  

@app.route('/')  
def home():   
    if 'email' in session:
        email = session['email'] 
        return render_template('Web_ini_logged.html',user = email)
    else:
        n = get_rand_number()
        return render_template('Web_ini.html',num = n)


@app.route('/login')  
def login(): 
    return render_template("login.html") 

@app.route('/success',methods = ["POST"])   
def success(): 
  if request.method == "POST":  
   session['email']=request.form['email']  
   return render_template('success.html')  


@app.route('/logout')  
def logout(): 
  if 'email' in session:  
    session.pop('email',None)  
    return render_template('logout.html');  

@app.route('/profile')  
def profile():  
   if 'email' in session:  
      email = session['email']  
      return render_template('profile.html',name=email) 

    
if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)
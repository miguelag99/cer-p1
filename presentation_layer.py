from flask import Flask, render_template, redirect, request, url_for, session, flash
from data_utils import get_rand_number


app = Flask(__name__)  
app.secret_key = "ayush"  

@app.route('/')  
def home():   
    #return render_template("homepage2.html")  
    n = get_rand_number()
    return "El num aleatorio obtenido es: {}".format(n)


    
if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)
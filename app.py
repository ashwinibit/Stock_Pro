from flask import Flask, render_template, request

import main_module


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    

@app.route("/get_input.html")

def input():
    return render_template("get_input.html")


@app.route("/", methods=["POST"])
def getValue():
    a1 = request.form['a1']
    a2 = request.form['a2']
    a3 = request.form['a3']
    a4 = request.form['a4']
    a5 = request.form['a5']
    a6 = request.form['a6']
    a7 = request.form['a7']
    a8 = request.form['a8']
    amt= request.form['amt']

   
    exp_ret, exp_vol, SR = main_module.insert_values(a1,a2,a3,a4,a5,a6,a7,a8,amt)
    
    return render_template("display.html",exp_ret=exp_ret, exp_vol=exp_vol, SR=SR, 
    a1=a1, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6, a7=a7, a8=a8)





    
if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, redirect, url_for, request, Response,session

name_k = "something" #will change for usr
app = Flask(__name__)
app.secret_key = "verysecretwewillchangethissoonlol"



def log_out():

    a=""
    session.pop(name_k, None)



@app.route('/', methods=["POST","GET"])
def home_page():
    # if name_k not in session:
    #     return url_for("set_name")
    if request.method == 'GET':
        return render_template("index.html")

    else:
        message = "message gotten : " + str(request.data)#getting the message
        print(str(request.form))
        #write_message to file
        #broadcast message
        print(message)
        return ('', 204) #returning nothing



@app.route('/work')
def work():
    print("CALLED PYTHON FROM JAVASCRIPT")
    return None
if __name__ == '__main__':
    app.run(debug=True)
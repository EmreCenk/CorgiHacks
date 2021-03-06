
from flask import Flask, render_template, redirect, url_for, request, Response,session

name_k = "something" #will change for usr
app = Flask(__name__)
app.secret_key = "verysecretwewillchangethissoonlol"


def log_out():
    session.pop(name_k, None)

@app.route('/')
def home_page():
    if name_k not in session:
        return url_for("set_name")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
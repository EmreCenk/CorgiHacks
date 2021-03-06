
from flask import Flask, render_template, redirect, url_for, request, Response,session
from server.client_side_sockets.client_class import client

print("this")
key_for_client_username  = "something" #will change for usr
app = Flask(__name__)
app.secret_key = "verysecretwewillchangethissoonlol"


def log_out():

    a=""
    session.pop(key_for_client_username, None)



@app.route('/', methods=["POST","GET"])
def home_page():
    if key_for_client_username not in session:
        session[key_for_client_username] = "Username9" #this will be customized once we have login page.

    # if key_for_client_username not in session:
    #     return url_for("set_name")

    if request.method == 'GET':
        if client is None:
            global current_client #we need to access this client object from the other functions as well
            current_client = client(username = session[key_for_client_username])

        return render_template("index.html")

    else:

        if client is None:
            #TODO: REDIRECT TO THE PAGE WHERE YOU CHOOSE A USERNAME
            
            return ('', 204) #returning nothing
        message = "message gotten : " + str(request.data)[1:] #getting the message that user wants to send
        client.send_message(self=client, msg=message) #sends the message
        return ('', 204) #returning nothing



@app.route('/work')
def work():
    print("CALLED PYTHON FROM JAVASCRIPT")
    return None
if __name__ == '__main__':
    app.run(debug=True)
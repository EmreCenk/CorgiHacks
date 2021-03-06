
from flask import Flask, render_template, redirect, url_for, request, Response,session,jsonify
from server.client_side_sockets.client_class import client
from time import sleep

key_for_client_username  = "something" #will change for usr
app = Flask(__name__)
app.secret_key = "verysecretwewillchangethissoonlol"
messages = []


def client_true():
    global current_client
    try:
        current_client
        return True
    except:
        return False

def log_out():

    a=""
    session.pop(key_for_client_username, None)

def disconnect_client():
    global current_client
    if client_true():
        current_client.disconnect()

@app.route('/', methods=["POST","GET"])
def home_page():
    global current_client  # we need to access this client object from the other functions as well

    if key_for_client_username not in session:
        session[key_for_client_username] = "Username9" #this will be customized once we have login page.

    # if key_for_client_username not in session:
    #     return url_for("set_name")



    if request.method == 'GET':
        if not client_true():
            current_client = client(username=session[key_for_client_username])

        return render_template("index.html")

    else:
        if len(request.data)<3:
            return ('', 204)  # returning nothing

        if not client_true():
            #TODO: REDIRECT TO THE PAGE WHERE YOU CHOOSE A USERNAME
            current_client=client(session[key_for_client_username])




        message = str(eval(request.data)["username"]) #getting the message that user wants to send


        client.send_message(self = current_client, msg=message) #sends the message
        return ('', 204) #returning nothing



@app.route('/get_messages')
def get_messages():
    global messages
    return jsonify({"messages":messages})
def update_messages():
    go=True

    while go:
        if not client_true():continue #don't do anything, client has not been initialized yet

        new_msgs = current_client.get_messages() #get the new messages

        for msg in new_msgs:
            print(msg)
            if msg == "{nonoquitquitquit}":
                disconnect_client()
                go=False
                break



        sleep(0.2) #checks every 0.2 seconds
if __name__ == '__main__':
    app.run(debug=True)
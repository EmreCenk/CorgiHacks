
from flask import Flask, render_template, redirect, url_for, request, Response,session,jsonify
from server.client_side_sockets.client_class import client
from time import sleep
from threading import Thread

key_for_client_username  = "something" #will change for usr
app = Flask(__name__)
app.secret_key = "verysecretwewillchangethissoonlol"

global messages
try:messages #if messages is already initialized, do nothing
except:messages = []

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

        dict_given=eval(request.data)
        if "username" in dict_given:

            message = str(dict_given["username"]) #getting the message that user wants to send


            client.send_message(self = current_client, msg=message) #sends the message
            return ('', 204) #returning nothing

        elif "update" in dict_given:
            global messages
            
            return messages


@app.route('/get_messages')
def get_messages():
    global messages
    return jsonify({"messages":messages})
def update_messages():
    global messages

    messages = []

    go=True

    while go:
        if not client_true(): continue #client is not initialized, don't bother doing anything
        new_messages = current_client.get_messages()
        messages.extend(new_messages) #add all of the messages in new messages

        for msg in new_messages:
            if msg=="{nonoquitquitquit}":
                #this message is sent when you quit
                disconnect_client()
                go=False
                break

        while len(messages)>50:
            messages.pop(0)



        sleep(0.2) #checks every 0.2 seconds






if __name__ == '__main__':
    Thread(target = update_messages).start() #start a thread constantly checking messages

    app.run(debug=True)

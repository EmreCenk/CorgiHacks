
from flask import Flask, render_template, redirect, url_for, request, Response,session,jsonify
from server.client_side_sockets.client_class import client
from time import sleep
from threading import Thread
global messages
global current_client

key_for_client_username  = "something" #will change for usr
app = Flask(__name__)
app.secret_key = "verysecretwewillchangethissoonlol"


try:messages #if messages is already initialized, do nothing
except:messages = []




@app.route("/api/get_real_messages", methods=["GET"])
def get_real_messages():
    global messages
    print(messages)
    tosend = {}
    i = 0
    for m in messages:
        i += 1
        tosend[str(i)] = m

    print(tosend)
    return tosend


def client_true():

    try:
        current_client
        return True

    except:return False

def log_out():

    a=""
    session.pop(key_for_client_username, None)

def disconnect_client():
    global current_client
    if client_true():
        current_client.disconnect()

@app.route('/', methods=["POST","GET"])
def home_page():
    global current_client

    if key_for_client_username not in session:
        session[key_for_client_username] = "Username9" #this will be customized once we have login page.

    # if key_for_client_username not in session:
    #     return url_for("set_name")



    if request.method == 'GET':
        if not client_true():
            current_client = client(username=session[key_for_client_username])
            # session['client']=current_client
            print("client initialized1")

        print("this")
        return render_template("index.html")

    else:
        print("not this")
        if len(request.data)<3:
            return ('', 204)  # returning nothing

        if not client_true():
            #TODO: REDIRECT TO THE PAGE WHERE YOU CHOOSE A USERNAME
            current_client=client(session[key_for_client_username])
            session['client'] = current_client
            print("client initialized2",current_client.username)

        dict_given=eval(request.data)
        if "username" in dict_given:

            message = str(dict_given["username"]) #getting the message that user wants to send


            client.send_message(self = current_client, msg=message) #sends the message
            return ('', 204) #returning nothing

        # elif "update" in dict_given:
        #     global messages
        #     tosend={}
        #
        #     i=0
        #     for m in messages:
        #         i+=1
        #         tosend[str(i)]=m
        #
        #     print(tosend)
        #
        #     return tosend

        return ('',204)


@app.route('/get_messages')
def get_messages():
    global messages
    return jsonify({"messages":messages})
def update_messages():
    global messages
    global current_client

    messages = []

    go=True

    while go:
        if not client_true():
            # print("client not init lol")
            sleep(0.5)
            continue #client is not initialized, don't bother
        # nything
        new_messages = current_client.get_messages()
        messages.extend(new_messages) #add all of the messages in new messages

        for msg in new_messages:
            print(msg)
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

import os
from flask import Flask, render_template, redirect, url_for, request, Response
from image_api import image_api_blueprint, db

app = Flask(__name__)
app.register_blueprint(image_api_blueprint)



from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from threading import Thread

#THESE ARE THE GLOBAL VARIABLES THAT WILL BE USED THROUGHOUT THE ENTIRE CODE
host= "localhost"
port=5500
buffer_size=512
ADDRESS=(host, port)

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

server.bind(ADDRESS)
connection_num=5

users = []

class user:
    def __init__(self, address, client):
        self.address = address
        self.client = client
        self.name = ""

    def set_name(self, name):
        self.name = name

def send_to_everyone(text, name):
    #this function will broadcast the sent messages to everyone in the room

    for user in users:
        #going through every user to send them the message
        client= user.client
        client.send(bytes(name + ": "+ text, "utf8"))


def client_com(user):
    #This is the thread to handle the messages that the client sends
    go=True

    client=user.client


    name = client.recv(buffer_size).decode("utf8")  # the user's name
    joined=f"{name} is in the chat"
    send_to_everyone(joined,"") #Tell everyone who has joined

    user.set_name(name=name)
    print(f"We are starting com with {user.name}")

    while go:
        try:
            msg=client.recv(buffer_size).decode("utf8")

            if msg == "{nonoquitquitquit}":
                users.remove(user) #removing user from the array of users
                send_to_everyone(f"{name} has left the chat...","")
                client.close()
                go=False #At this point the user has exited, so we need to stop this thread

            else:

                print(f"{name} : ", msg)
                send_to_everyone(msg, name)
        except Exception as problem:
            print(users,problem)
            users.pop(users.index(user))
            go=False #The person has disconnected


def wait_to_connect(server):

    #Wait for a new client to connect. Once connected, start a new thread.
    #going on an infinite loop to wait for connections
    go=True

    while go:

        try:
            client, client_address = server.accept()
            current_user=user(client_address,client)
            users.append(current_user) #appending the user object to the array of users

            print(f"{client_address} has connected!")
            Thread(target=client_com,args=(current_user,)).start() #Starts a thread that waits for the client to send
            # a message


        except Exception as problem:
            print("Something has gone wrong2: " + str(problem))

            go=False



from flask import Flask, render_template, redirect, url_for, request, Response,session,jsonify
from client_class import client
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
        tosend[i] = m
        i += 1

    if tosend=={}:
        tosend={0:""}
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




# Fallback route if they just type something random
@app.route("/*")
def undefined_page():
    return redirect(url_for("home_page"))



def everything():
    global app

    Thread(target = update_messages).start() #start a thread constantly checking messages
    app.run(debug=True)

if __name__=="__main__":

    def yes():

        connection_num=5
        server.listen(connection_num) #listen for 'connection_num' connections
        print("waiting for connection")
        accept_thread=Thread(target=wait_to_connect(server=server), args=(server,)) #there is a comma after

        # server bc the


    alpha=Thread(target=yes).start()
    everything()






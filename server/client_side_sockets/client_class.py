

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class client:
    """Yay we communicate with server"""

    host = "localhost"
    port = 5500
    address = (host, port)
    buffer_size = 512

    def __init__(self, username):
        #Initialize person
        
        self.socket_of_client = socket(AF_INET, SOCK_STREAM)
        self.socket_of_client.connect(self.address)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(username)
        self.lock = Lock()

    def receive_messages(self):
        """
        Get messages from server
        """
        while True:
            try:
                msg = self.socket_of_client.recv(self.buffer_size).decode()

                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("Oh st, something went wrong ", e)
                break

    def send_message(self, msg):
        """
        sends a message to the server

        """
        try:
            self.socket_of_client.send(bytes(msg, "utf8"))
            if msg == "{quitquitquit}":
                self.socket_of_client.close()
                
        except Exception as e:
            #something didn't work, we try it again
            self.socket_of_client = socket(AF_INET, SOCK_STREAM)
            self.socket_of_client.connect(self.address)
            print(e)

    def get_messages(self):
        """
        gets a list of messages 

        """
        messages_copy = list(self.messages) #creating a copy of the messages

        # check memory
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy
    
    def disconnect(self):
        self.send_message("{quitquitquit}")
from threading import Thread
from socket import *
import select
import sys


ip= "0.0.0.0"
port = "55010"

#here we create the socket, sock_stream means it tcp protocol
soc = socket(AF_INET, SOCK_STREAM)

#
soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

#here we bind the ip to the port number
soc.bind((ip,int(port)))

#this server can listen up to 50 clients
soc.listen(50)
print("Listening...")

#dictionery to store all the online clients
clients = {}

def clientListen(cl):

    while True:
        try:
            message = cl.recv(1024).decode()

            first_word = message.split()[0]
            message=message.replace(first_word,"")

            if first_word == "broadcast":
                broadcast(message,cl)

            if first_word == "addC":
                clients[message]=cl

            else:
                if clients.get(first_word)==None:
                    cl.se

        except Exception as e:
            print(f"Error {e}")

#this method is sending a bordcast message to the chat room
def broadcast(msg, sourceSocket):
    for c in clients.values():
        # and send the message
        if c != sourceSocket:
            try:
                clients.send(msg)
            except:
                clients.close()


while True:
    conn, addr = soc.accept()

    print(addr[0] + " is connected")

    Thread(clientListen, (conn, addr))

soc.close()
# This prrogrem will implement a client side in simple chat

import socket
import select
import threading

## the first thing entering a chat is to choose your nickname
name_or_nickname = input("please enter your display name : ").strip()
while not name_or_nickname:
    name_or_nickname = input("you must fill this with your choise: ").strip()

#defining the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "Chathost" # "128.0.1.1"
port =55010

#conecting to the server
server.connect(host,port)

## that alowes the client to send messages multiple messages to the server
def thread_sender():
    while True:
        send_a_message = input("please entet ypur message :")
        server.send(send_a_message.encode())

## that alowes the client to recive massage from the server

def thread_recive_a_massage():
    while True:
        recived = server.recv(1024).decode()
        print(recived)

thread_send = threading.Thread(target=thread_send())
thread_reciver = threading.Thread(target= thread_recive_a_massage())
thread_send.start()
thread_reciver.start()

# ask_for_download


##
)
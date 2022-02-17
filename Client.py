# This prrogrem will implement a client side in simple chat

import socket
from threading import Thread

# this method getting the first command
def geting_info():
    global str, name, command

    str = input().strip()
    try:
        command = str.split()[0]
        name = str.split()[1]

    except Exception as e:
        print(e)

    while not str or command!="connect" or name==None:
            str = input().strip()
            try:
                command = str.split()[0]
                name = str.split()[1]
            except Exception as e:
                print(e)

geting_info()

#defining the server socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port =55010

#conecting to the server
soc.connect((host,port))

#adding the new user
c = f"addC "+ name
soc.send(c.encode())

def messagesListener():
    while True:
        msg = soc.recv(1024).decode()
        print(msg)

# creating new thread for each client messages
th = Thread(target=messagesListener)
# make the thread run until the main thread die
th.daemon = True

th.start()

while True:
    # getting the message
    msg =  input()

    soc.send(msg.encode())

# close the socket
soc.close()

# ask_for_download


##

import socket
from threading import Thread
import os

import sender

ip = "0.0.0.0"
port = 55010

#dictionery of all the online clients
client_sockets = {}

#making TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind ip and port
s.bind((ip, port))

# listen for upcoming connections
s.listen(50)
print("Listening...")

#this method returns the name of the user by its socket
def findBySocet(so):
    for k, v in client_sockets.items():
        if v==so:
            return k

#this method is sending the message for every online person
def broadcast(msg):
    for c in client_sockets.values():
        try:
            c.send(msg.encode())
        except Exception as e:
            print("error "+ e)

#this method send to a specific person a message
def sendTo(msg, to):
    s = client_sockets.get(to)
    if s!=None:
        s.send(msg.encode())
        print(f"sending to {to}: {msg}")

#this method returns list of the online users
def getList(d):
    l = None
    for k in d.keys():
        if l==None:
            l=k;
        else:
            l=f"{l},{k}"
    return l

#this method is listening for clients
def clientListen(cl, cAddr):
    while True:
        try:
            msg = cl.recv(1024).decode()

        except Exception as e:
            print("Error: " + e)

        print(msg)

        source = findBySocet(cl)

        first_word = msg.split()[0]
        msg = msg.replace(first_word+" ", "",1)

        # sending the message for every online person
        if first_word == "set_msg_all":
            msg= f"{source}: {msg}"
            broadcast(msg)
            print("sending broadcast massage: "+ msg)

        # adding a new client to the dict
        elif first_word == "addC":
            first_word = msg.split()[0]

            client_sockets[first_word] = cl
            print("Adding new Client: "+first_word)
            broadcast("new Client: "+first_word)

        # sending a message to a specific person
        elif first_word=="set_msg":
            first_word = msg.split()[0]
            msg = msg.replace(first_word+" ", "",1)
            msg = f"{source}: {msg}"

            sendTo(msg,first_word)

        elif first_word == "get_users":
            l = getList(client_sockets)
            print(l)
            cl.send(l.encode())

            print("returning the online people: "+l)

        elif first_word == "get_list_file":
            files = str(os.listdir('.'))
            print("The files are: "+files)
            cl.send(files.encode())

        elif first_word == "disconnect":
            n=""
            for name, soc in client_sockets.items():
                if cl==soc:
                    broadcast("disconnected: " + name)

                    soc.close()
                    client_sockets.pop(name)
                    print("disconnecting: " + name)


        elif first_word== "download":
            files = os.listdir('.')

            if msg in files:
                cl.send(("sending file: "+msg).encode())
                print("asking to download: "+ msg)
                sender.theSender(msg,cAddr[0])
            else:
                cl.send("There is no such file.".encode())

while True:
    #accepting the data that was sent to the server
    cSoc, cAddress = s.accept()

    cSoc.send("connected".encode())

    #creating new thread for each client messages
    th = Thread(target=clientListen, args=(cSoc,cAddress))

    #make the thread run until the main thread die
    th.daemon = True
    # start the thread
    th.start()

#closing the sockets
for cs in client_sockets:
    cs.close()

s.close()

import socket
from threading import Thread


ip = "0.0.0.0"
port = 55010

#dictionery of all the online clients
client_sockets = {}

#making TCP socket
s = socket.socket()

# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind ip and port
s.bind((ip, port))

# listen for upcoming connections
s.listen(50)
print("Listening...")

#this method is sending the message for every online person
def broadcast(msg, source):
    for c in client_sockets:
        c.send(msg.encode())

#this method send to a specific person a message
def sendTo(msg, to):
    s = client_sockets.get(to)
    if s!=None:
        s.send(msg.encode())
        print(f"sending to {to}: {msg}")

#this method is listening for clients
def clientListen(cl):
    while True:
        try:
            msg = cl.recv(1024).decode()

        except Exception as e:
            print(" Error: " + e)

        print(msg)

        first_word = msg.split()[0]
        msg = msg.replace(first_word+" ", "")

        # sending the message for every online person
        if first_word == "$broadcast":
            broadcast(msg, cl)
            print("sending broadcast massage: "+ msg)

        # adding a new client to the dict
        elif first_word == "$addC":
            first_word = msg.split()[0]

            client_sockets[first_word] = cl
            print("Adding new Client: "+first_word)

        # sending a message to a specific person
        elif first_word=="$sendTo":
            first_word = msg.split()[0]
            msg = msg.replace(first_word+" ", "")

            sendTo(msg,first_word)

        elif first_word == "$get_users":
            l = client_sockets.keys().__str__()
            print(l)
            cl.send(l.encode())

            print("returning the online people: "+l)

        elif first_word == "$disconnect":


            print("returning the online people: " + l)

while True:
    #accepting the data that was sent to the server
    cSoc, cAddress = s.accept()
    print(f"{cAddress} connected.")

    #creating new thread for each client messages
    t = Thread(target=clientListen, args=(cSoc,))

    #make the thread run until the main thread die
    t.daemon = True
    # start the thread
    t.start()

#closing the sockets
for cs in client_sockets:
    cs.close()

s.close()

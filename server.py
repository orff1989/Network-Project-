import socket
from threading import Thread
import os

############################################# SENDER###############################

# this method prevent calculate ord of int instead of char
def ordHelper(n):
    if type(n) == int:
        return n
    else:
        return ord(n)


# this method calculate the checksum of a message
def checksumCalculator(msg):
    index = len(msg)
    if (index & 1):
        index -= 1
        sum = ordHelper(msg[index])
    else:
        sum = 0

    # calculating the checksum
    while index > 0:
        index -= 2
        sum += (ordHelper(msg[index + 1]) << 8) + ordHelper(msg[index])

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    ans = (~ sum) & 0xffff
    ans = ans >> 8 | ((ans & 0xff) << 8)

    return chr(int(ans / 256)) + chr(ans % 256)


# this method sends the file to the client
def theSender(nameOfFile, ip):

    buffSize = 200

    PortSend = 55006
    PortRecv = 55005

    recvT = (ip, PortRecv)
    destT = (ip, PortSend)

    # reading the file
    with open(nameOfFile) as f:
        data = f.read()

    # getting the size of the file
    size = os.path.getsize(nameOfFile)
    data = str(size) + str(" ") + data

    # adding ~ to the end of the data
    data = data + " ~"

    # creating the sender and receiver socket
    socketSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketReceiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # binding the socket
    socketReceiver.bind(recvT)

    # setting timeout
    socketReceiver.settimeout(1)

    pos = 0
    sequence = 0

    while pos < len(data):

        # putting the data to send in the buffer
        if pos + buffSize > len(data):
            buff = data[pos:]
        else:
            buff = data[pos:pos + buffSize]
        pos += buffSize

        gotAck = False
        while not gotAck:
            m = str(checksumCalculator(buff)) + str(sequence) + str(buff)
            socketSender.sendto(m.encode(), destT)

            try:
                # receiving the data from the sender
                theMsg, address = socketReceiver.recvfrom(4096)
                theMsg = theMsg.decode()

            except socket.timeout:
                print("Timeout")

                if buffSize > 100:
                    buffSize = buffSize / 2
            else:

                checksum = theMsg[:2]
                ack_seq = theMsg[5]
                theMsg = theMsg[2:]

                print(theMsg)

                # checking if the checksum is equal to what we got
                if checksumCalculator(theMsg) == checksum and ack_seq == str(sequence):
                    gotAck = True

                    if buffSize <= 2000:
                        buffSize = buffSize * 2

        # changing the predicted sequence to the other one: 1->0, 0->1
        sequence = (sequence + 1) % 2


################################ SERVER #####################################
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
                    theSender(msg,cAddr[0])
                else:
                    cl.send("There is no such file.".encode())

        except Exception as e:
            print("Error: " + e)
while True:
    try:
        # accepting the data that was sent to the server
        cSoc, cAddress = s.accept()

        cSoc.send("connected".encode())

        # creating new thread for each client messages
        th = Thread(target=clientListen, args=(cSoc,cAddress))

        # make the thread run until the main thread die
        th.daemon = True
        th.start()

    except Exception as e:
        print(e)

#closing the sockets
for cs in client_sockets:
    cs.close()

s.close()

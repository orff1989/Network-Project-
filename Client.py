import socket
from threading import Thread

# this method getting the first command
import receiver


def geting_info():
    global str, name, command

    str = input().strip()
    try:
        command = str.split()[0]
        name = str.split()[1]

    except Exception as e:
        print(e)

# def sendFile():
#     while not str or command!="connect" or name==None:
#             str = input().strip()
#             try:
#                 command = str.split()[0]
#                 name = str.split()[1]
#             except Exception as e:
#                 print(e)

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

        if msg[:13] == "sending file:":

            print("start download: "+ msg[14:])
            th2 = Thread(target=receiver.recvFile(msg[14:],host))
            th2.daemon = True
            th2.start()

# creating new thread for each client messages
th1 = Thread(target=messagesListener)


# make the thread run until the main thread die
th1.daemon = True


th1.start()


while True:
    # getting the message
    msg = input()
    soc.send(msg.encode())

    # if msg.split()[0]=="download":
    #
    #     th2 = Thread(target=receiver.recvFile(msg.split()[1],host))
    #     th2.daemon = True
    #     th2.start()

# close the socket
soc.close()






import socket
from threading import Thread
import os

# ------------------------#
server_IP = "127.0.0.1"

server_PORT = 55010
# ------------------------#


######################################### receiver ########################################################

#this method prevent calculate ord of int instead of char
def ordHelper(n):
    if type(n)==int:
        return n
    else:
        return ord(n)

# this method calculate the checksum of a message
def checksumCalculator(msgg):
    index = len(msgg)
    if (index & 1):
        index -= 1
        sum = ordHelper(msgg[index])
    else:
        sum = 0

    # calculating the checksum
    while index > 0:
        index -= 2
        sum += (ordHelper(msgg[index + 1]) << 8) + ordHelper(msgg[index])

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    ans = (~ sum) & 0xffff
    ans = ans >> 8 | ((ans & 0xff) << 8)

    return chr(int(ans / 256)) + chr(ans % 256)


# this method sends message to the dest
def send(theSocket,theMessage, theDest):
    checksum = checksumCalculator(theMessage)
    theData = str(checksum) + str(theMessage)
    theSocket.sendto(theData.encode(), theDest)


# this method gets the file that was sent
def recvFile(fileName, ip):

    PortSend = 55005
    PortRecv = 55006

    recvT = ("0.0.0.0", PortRecv)
    destT = (ip, PortSend)

    # creating the sender and receiver socket
    socketSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketReceiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # binding the socket
    socketReceiver.bind(recvT)

    predictedSeq = 0
    print("receiving...")
    done=False
    size=None
    while True:
        # receiving the data from the sender
        theMsg, addr = socketReceiver.recvfrom(4096)
        theMsg= theMsg.decode()

        # getting the checksum
        checksum = theMsg[:2]
        sequence = theMsg[2]

        theMsg = theMsg[3:]

        # if received all the data it will be true
        if theMsg.split()[-1] == "~":
            done=True

        # checking if the checksum is equal to what we got
        if checksumCalculator(theMsg) == checksum:

            send(socketSender,"ACK" + sequence, destT)

            # checking if the the sequence is the predicted one
            if sequence == str(predictedSeq):

                if size==None:
                    size = int(theMsg.split()[0])
                    theMsg = theMsg.replace(str(size) + " ", "", 1)

                theMsg = theMsg.replace(" ~", "")

                # open new file and copy the data to it
                with open(fileName, 'a') as f:
                    f.write(theMsg)

                print(theMsg)

                currSize = os.path.getsize(fileName)
                prec = 100 * currSize / size

                print("You downloaded " + str("{:.2f}".format(prec)) + "% out of file. Last byte is: " + str(
                    currSize) + ".")

                # changing the predicted sequence to the other one: 1->0, 0->1
                predictedSeq = (predictedSeq +1)%2

                # true if got all the data that was sent
                if done:
                    break

        else:
            NAK = str((predictedSeq+1)%2)
            send(socketSender, "ACK" + NAK, destT)


################################################# Client #####################################################
class Client:

    def __init__(self):
        print("Client created")

    def geting_info(self):
        global name, command

        info = input().strip()
        try:
            command = info.split()[0]
            name = info.split()[1]

        except Exception as e:
            print(e)

    # this method connects to the server
    def connect_to_server(self,host,port):
        # defining the server socket
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # conecting to the server
        self.soc.connect((host, port))

        # adding the new user
        c = f"addC " + name
        self.soc.send(c.encode())

    # this method listens to the messages
    def messagesListener(self):
        while True:
            msg = self.soc.recv(1024).decode()

            if msg[:13] == "sending file:":
                try:
                    th2 = Thread(target=recvFile(msg[14:], server_IP))
                    th2.daemon = True
                    th2.start()

                except Exception as e:
                    print(e)

            else:
                print(msg)

    # this method gets the data and sends it
    def get_and_send(self):
        while True:
            # getting the message
            try:
                msg = input()
                self.soc.send(msg.encode())

            except Exception as e:
                print(e)

        # close the socket
        self.soc.close()

    # this method connect entirely to the server
    def join_to_server(self):
        self.geting_info()

        host = server_IP
        port = server_PORT

        self.connect_to_server(host, port)

        # creating new thread for each client messages
        th1 = Thread(target=self.messagesListener, )

        # make the thread run until the main thread die
        th1.daemon = True
        th1.start()

        self.get_and_send()

if __name__ == '__main__':
    c= Client()
    c.join_to_server()









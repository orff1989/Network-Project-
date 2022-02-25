import socket
import os

#this method prevent calculate ord of int instead of char
def ordHelper(n):
    if type(n)==int:
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
    data = str(size) + str(" ")+ data

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
            m= str(checksumCalculator(buff)) + str(sequence) + str(buff)
            socketSender.sendto(m.encode(), destT)

            try:
                # receiving the data from the sender
                theMsg, address = socketReceiver.recvfrom(4096)
                theMsg=theMsg.decode()

            except socket.timeout:
                print("Timeout")

                if buffSize>100:
                    buffSize=buffSize/2
            else:

                checksum = theMsg[:2]
                ack_seq = theMsg[5]
                theMsg=theMsg[2:]

                print(theMsg)

                # checking if the checksum is equal to what we got
                if checksumCalculator(theMsg) == checksum and ack_seq == str(sequence):
                    gotAck = True

                    if buffSize<=2000:
                        buffSize=buffSize*2

        # changing the predicted sequence to the other one: 1->0, 0->1
        sequence = (sequence +1)%2



if __name__ == '__main__':
    theSender('file.txt','127.0.0.1')
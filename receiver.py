import socket

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

# this method sends message to the dest
def send(theSocket,theMessage, theDest):
    checksum = checksumCalculator(theMessage)
    theSocket.sendto((str(checksum) + theMessage).encode(), theDest)

# this method gets the file that was sent
def recvFile(fileName, ip):

    PortSend = 55005
    PortRecv = 55006

    recvT = (ip, PortRecv)
    destT = (ip, PortSend)

    # creating the sender and receiver socket
    socketSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketReceiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # binding the socket
    socketReceiver.bind(recvT)

    predictedSeq = 0
    print("receiving...")
    done=False

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
                theMsg = theMsg.replace(" ~","")

                # open new file and copy the data to it
                with open(fileName, 'a') as f:
                    f.write(theMsg)

                print(theMsg)
                # changing the predicted sequence to the other one: 1->0, 0->1
                predictedSeq = (predictedSeq +1)%2

                # true if got all the data that was sent
                if done:
                    break

        else:
            NAK = str((predictedSeq+1)%2)
            send("ACK" + NAK, destT)

if __name__ == '__main__':
    recvFile('ch.txt','127.0.0.1')
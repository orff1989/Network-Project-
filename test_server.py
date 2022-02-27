import unittest
from socket import socket

import server
MSG = "hi everyone have tou received"
first_word = input()

class SocketPairTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
            unittest.TestCase.__init__(self, methodName=methodName)

    def setUp(self):
            self.serv, self.cl = socket.socketpair()


    def testSendAll(self):
            # Testing sendall() with a 2048 byte string over TCP
            msg = ''
            while 1:
                read = self.cl_conn.recv(1024)
                if not read:
                    break
                msg += read
            self.assertEqual(msg, 'f' * 2048)
    def _testSendAll(self):
            size_msg = 'f' * 2048
            self.serv_conn.sendall(size_msg)


    def testShutdown(self):
            # Testing shutdown()
            msg = self.cl_conn.recv(1024)
            self.assertEqual(msg, MSG)
            self.done.wait()

    def _testShutdown(self):
            self.serv_conn.send(MSG)
            self.serv_conn.shutdown(2)


    def test_msg_pass(self):
        msg = self.conn.recv(1024)
        self.assertEqual(msg, MSG)
        self.assertEqual(self.claddr, self.connaddr)

    def test_msg_pass(self):
        self.cl.send(MSG)
        self.cl.close()

if __name__ == '__main__':
    unittest.main()

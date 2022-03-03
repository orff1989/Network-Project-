import socket
import socketserver
import unittest
import Client
## i'm not sure this is needed !!!!!!!!!!
class TestServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

class MyTestCase(unittest.TestCase):

    # def setUp(self):
    #     self.server = TestServer((HOST, PORT), MyTestCase)
    #     client_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # client_socket.connect((host,  Client.Client.connect_to_server.port))
    #     # self.server = TestServer((HOST, PORT), MyRequestHandler)
    #     self.client = socket.create_connection((HOST, PORT))

    def tearDown(self):
        self.client_socket.close()
        self.server.shutdown()
        self.server.server_close()

    def test_sendTo(self):
        self.soc.sendTo(c .encode())
        self.assertEqual(self.client_socket.recv(1024).decode(), 'reply1')

    def test_2(self):
        self.client_socket.send('message2'.encode())
        self.assertEqual(self.client_socket.recv(1024).decode(), 'reply2')

if __name__ == '__main__':
    unittest.main()

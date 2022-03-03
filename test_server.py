import unittest
import socket

import server
from Client import Client as testClient
from server import Server as testServer

class MockInputFunction:
    def __init__(self, return_value=None):
        self.return_value = return_value
        self._orig_input_fn = __builtins__['input']

    def _mock_input_fn(self, prompt):
        print(prompt + str(self.return_value))
        return self.return_value

    def __enter__(self):
        __builtins__['input'] = self._mock_input_fn

    def __exit__(self, type, value, traceback):
        __builtins__['input'] = self._orig_input_fn
#
class ServerTest(unittest.TestCase):

     def setUp(self):
        # ------------------------#
        server_IP = "127.0.0.1"

        server_PORT = 55010
        # ------------------------#
        self.cadd = (server_IP,server_PORT)
        self.my_server = testServer()
        self.my_server.making_server()
        self.client1 = testClient()
#
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((server_IP, server_PORT))
        self.client1.connect_to_server(server_IP,server_PORT, 'gil')

     def test_msg_to_all(self):
        testServer.clientListen()
        x = input("msg_to_all")
        return int(x)

        with MockInputFunction(return_value='sending broadcast massage'):
            assert test_msg_to_all() == 'msg_to_all'

     def test_msg_to_one():
            testServer.clientListen()
            x = input("msg_to")
            return int(x)

     with MockInputFunction(return_value="massage sent to "):
            assert test_msg_to_all() == 'connect'

    def test_get_users():
       testServer.clientListen()
       x = input("get_users")
       return int(x)

    with MockInputFunction(return_value='returning the online people'):
    assert test_msg_to_all() == 'get_users'

 def test_get_users():
            testServer.clientListen()
            x = input("get_users")
            return int(x)

        with MockInputFunction(return_value='returning the online people'):
                assert test_msg_to_all() == 'get_users'


#         c = f"connect " + 'gil'
#         self.soc.send(c.encode())
#
#     def tearDown(self):
#         self.soc.close()
#
#
#     def test_make_server(self):
#         self.assertEqual(testServer.making_server(self), 'Listening')
#
#     def test_client_listen(self):
#         msg = 'set_msg_all'
#         self.soc.send(msg.encode())
#         testServer.clientListen(self, self.soc, self.cadd)
        #self.assertEqual(output, 'Listening')

    # def test_2(self):
    #     self.client_socket.send('message2'.encode())
    #     self.assertEqual(self.client_socket.recv(1024).decode(), 'reply2')


if __name__ == '__main__':
    unittest.main()

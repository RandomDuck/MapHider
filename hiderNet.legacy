import socket
from time import ctime
class client():
    def __init__(self):
        # create an INET, STREAMing socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # now connect to the web server on port 80 - the normal http port
        port=1280
        host="127.0.0.1"
        print(host)
        s.connect((host, port))
        while True:
            s.send(input().encode())
            data=s.recv(2000).decode()  
            print(data)

    def connect(self):
        pass
    def send(self):
        pass
    def recive(self):
        pass

class server():
    def __init__(self):
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        port=1280 
        serversocket.bind(("127.0.0.1", port))
        # become a server socket
        serversocket.listen(5)
        while True:
            # accept connections from outside
            (clientsocket, address) = serversocket.accept()
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server
            print("\nclient connected with.\nAdress:\n",address)
            while True:
                data=clientsocket.recv(2000).decode()    
                if not data:
                    break
                string="[%s] %s" % (ctime(), data)
                clientsocket.send(string.encode())
                print(data)

    def senddata(self):
        pass
    def sendclr(self):
        pass
    def setup(self):
        pass
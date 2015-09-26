'''
A simple "echo" client written in Python.

author:  Amy Csizmar Dalal and [YOUR NAMES HERE]
CS 331, Fall 2015
date:  21 September 2015
'''
import sys, socket

class GopherTCPClient:

    def __init__(self, requeststring, host="",port=50000):
        self.port = port
        self.host = host
        self.write_buffer=requeststring
        self.clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect()
        self.connection_loop()

    def connect(self):
        try:
            self.clientsock.connect((self.host, self.port))
            print ("Connected to server;")
            self.clientsock.send(requeststring.encode("ascii"))
            print ("Sent message; waiting for reply")
            response=self.clientsock.recv(1024)
        except socket.error:
            print("Could not connect to server")
            sys.exit(1)
        if response is not None:
            response=response.decode("ascii")
            self.handle_response(response)
            #connection terminated by server, enter new connection loop

    def connection_loop(self):
        while True:
            request=input("Enter request: ")
            self.write_buffer=request
            self.connect()
    def handle_response(self, response):
        print(response)



def usage():
    print ("Usage:  python SimpleTCPClient <server IP> <port number> <message>")

def main():
    # Process command line args (server, port, message)
    if len(sys.argv) == 4:
        try:
            server = sys.argv[1]
            port = int(sys.argv[2])
            message = sys.argv[3]
            GopherTCPClient(message,server,port)
        except ValueError:
            usage()


        serverSock.send(message.encode("ascii"))

        returned = serverSock.recv(1024)
        print ("Received reply: "+ returned.decode("ascii"))

        serverSock.close()

    else:
        usage()

main()

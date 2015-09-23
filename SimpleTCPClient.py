'''
A simple "echo" client written in Python.

author:  Amy Csizmar Dalal and [YOUR NAMES HERE]
CS 331, Fall 2015
date:  21 September 2015
'''
import sys, socket

class GopherTCPClient:

    def __init__(self, host="",port=50000,requeststring):
        self.port = port
        self.host = host
        self.clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clientsock.connect((self.host, self.port))
        self.clientsock.send(requeststring.encode("UTF8"))
        response=self.clientsock.recv(1024)
        #make response pretty




def usage():
    print ("Usage:  python SimpleTCPClient <server IP> <port number> <message>")

def main():
    # Process command line args (server, port, message)
    if len(sys.argv) == 4:
        try:
            server = sys.argv[1]
            port = int(sys.argv[2])
            message = sys.argv[3]
        except ValueError:
            usage()

        serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSock.connect((server, port))
        print ("Connected to server; sending message")

        serverSock.send(message.encode("ascii"))
        print ("Sent message; waiting for reply")

        returned = serverSock.recv(1024)
        print ("Received reply: "+ returned.decode("ascii"))

        serverSock.close()

    else:
        usage()

main()
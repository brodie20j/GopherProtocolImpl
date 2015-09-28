'''
A Gopher client written in Python.

author:  Amy Csizmar Dalal, Jonathan Brodie, Camille Benson, Tristan Leigh
CS 331, Fall 2015
date:  21 September 2015
'''
import sys, socket

class GopherTCPClient:

    def __init__(self, requeststring, host="",port=50000):

        self.port = port
        self.host = host
        self.write_buffer=requeststring
        self.clientsock = None
        self.connect()
        self.connection_loop()

    def connect(self):
        '''
        Connection function that attempts to connect to the server and send
        the write buffer over the wire
        '''
        try:
            self.clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.clientsock.connect((self.host, self.port))
            print ("Connected to server;")
            self.clientsock.send(self.write_buffer.encode("ascii"))
            print ("Sent message; waiting for reply")
            response=self.clientsock.recv(32768)
            print("Received response from the server:\n")
        except socket.error:
            print("Could not connect to server")
            sys.exit(1)
        if response is not None:
            response=response.decode("ascii")
            self.handle_response(response)
        else:
            print("The connection was terminated!  Closing client.")
            sys.exit(1)
            #connection terminated by server, enter new connection loop

    def connection_loop(self):
        '''
        Client connection loop.  Gets input to put on the write buffer and
        then connects to the server
        '''
        while True:
            request = input("Enter request as follows:\n>>FilePath<CR><LF>\n>>")
            self.write_buffer = request
            self.connect()


    def handle_response(self, response):
        '''
        Handles the server's response and properly formats it.
        '''
        response=response.split("<CR><LF>")
        for line in response:
            # Specify file type
            if len(line) > 0 and line != ".":
                file_type = line[0]
                if file_type == '1':
                    line = "Directory: "+line[1:]
                    line = line.split('\t')
                    print(line[0]+"\t"+line[1])
                elif file_type == '0':
                    line = "File: "+line[1:]
                    line = line.split('\t')
                    print(line[0]+"\t"+line[1])
                else:
                    print(line)


def usage():
    print ("Usage:  python SimpleTCPClient <server IP> <port number> <message>")


def main():
    # Process command line args (server, port, message)
        try:
            server = sys.argv[1]
            port = int(sys.argv[2])
            message = sys.argv[3]
            GopherTCPClient(message,server,port)
        except ValueError:
            usage()

main()

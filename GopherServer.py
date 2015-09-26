'''
A Gopher server written in Python.

author:  Amy Csizmar Dalal, Jonathan Brodie, Camille Benson, Tristan Leigh
CS 331, Fall 2015
date:  21 September 2015
'''
import sys, os,socket

class GopherTCPServer:
    def __init__(self, port=50000):
        self.port = port
        self.host = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))


    def parse_client_request(self, data):
        terminatorstring="<CR><LF>"
        endindex=data.find(terminatorstring)
        if endindex == 0:
            return self.links_func()
        elif endindex == -1:
            self.error()
            return ""
        else:
            request=data[0:endindex]
            self.get_requested_data(request)
            #commented out because we only needed to finish 
            #newdata=data[endindex+len(terminatorstring):len(data)]
            #self.parse_client_request(newdata)

    def links_func(self):
        fyle = open("server.links")
        return fyle.read()

    def get_requested_data(self, data):
        sampleString=self.links_func()
        index=sampleString.find(data)

        if index == -1:
            #elegantly handle error
            self.error(data)
        else:
            #the request exists!
            file_type=data[0]
            if file_type == "0":
                #open the file and send it over
                print("foo")
            elif file_type == "1":
                #walk the directory and return all files and subdirectories there
                print("foo)")

    def error(self, request):
        #elegantly handles a file not found
        print("ERROR: "+request+"\nCould not be found!")

    def listen(self):
        self.sock.listen(5)

        while True:
            clientSock, clientAddr = self.sock.accept()
            print ("Connection received from ",  clientSock.getpeername())
            # Get the message and echo it back
            #while True:
            data = clientSock.recv(1024)
            if not len(data):
                break
            print ("Received message:  " + data.decode("ascii"))
            response=self.parse_client_request(data.decode("ascii"))
            clientSock.sendall(response.encode("ascii"))
            clientSock.close()
            print("Closed socket. Connection is over.")

def main():
    # Create a server
    if len(sys.argv) > 1:
        try:
            server = GopherTCPServer(int(sys.argv[1]))
        except ValueError:
            print ("Please specify port as an integer.  Creating server on default port.")
            server = GopherTCPServer()
    else:
        server = GopherTCPServer()

    # Listen forever
    print ("Listening on port " + str(server.port))
    server.listen()

main()

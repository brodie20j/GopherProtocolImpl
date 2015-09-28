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
        '''
        Parses the request the client sends over.  Returns the links file
        if the user sends a blank line.  Looks for specific otherwise
        '''
        terminatorstring = "<CR><LF>"
        endindex = data.find(terminatorstring)
        if (endindex >= 255):
            #selectionstring is too long!
            return "Request Error: Please limit selection string to less than 255 characters"

        if endindex == 0:
            return self.links_func()
        elif endindex == -1:
            self.error(data)
            return "Request Error: Please include <CR><LF> at the end of the command"
        else:
            request=data[0:endindex]
            return self.get_requested_data(request)


    def links_func(self):
        '''
        opens the links file and parses the new lines and replaces them with
        the terminator string
        '''
        f = open("server.links")
        return_string=""
        fyle=f.read()
        fyle=fyle.replace("\n\n","\n")
        fyle=fyle.replace("\n","<CR><LF>")

        return fyle+"."


    def get_requested_data(self, data):
        '''
        finds the requested data and returns it
        '''
        fyle = open("server.links")
        found = False
        requested_data = ""
        for line in fyle.readlines():

            index = line.find(data)

            if index > -1:
                file_type = line[0]
                request_string = line.split('\t')[1]
                print("RQ:",request_string)
                #the request exists!
                if not found:
                    if file_type == "0":
                        requested_data = open(data).read()
                        return requested_data

                found = True
                requested_data += line + "<CR><LF>"
        if found is False:
            return self.error(data)
        return requested_data + '.'

    def error(self, request):
        '''
        elegantly handles a file or directory not found
        '''
        print("ERROR: "+request+"\nCould not be found!")

    def listen(self):
        '''
        Server listening loop
        '''
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
            response = self.parse_client_request(data.decode("ascii"))
            print(response)
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

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
        print(data)
        print(len(data))
        terminatorstring = "\r\n"
        endindex = data.find(terminatorstring)
        if (endindex >= 255):
            #selectionstring is too long!
            return "Request Error: Please limit selection string to less than 255 characters"

        if endindex == 0:
            return self.links_func()
        elif endindex == -1:
            self.error(data)
            print("DATA:", data)
            error_message="Request Error: Please include \\r\\n at the end of the command"
            print(error_message)
            return error_message
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
        fyle=fyle.replace("\n","\r\n")

        return fyle+"."


    def get_requested_data(self, data):
        '''
        finds the requested data and returns it
        '''
        fyle = open("server.links")
        found = False
        requested_data = ""

        for line in fyle.readlines():
            # Find if data has exact match
            sample = line.split('\t')
            if len(sample) > 1:
                if data == sample[1] and not found:
                    #exact match!
                    if line[0] == '0':
                        requested_data = open(data).read()
                        print(requested_data)
                        return requested_data+"\r\n"
                    elif line[0] == '1':
                        requested_data+=line+"\r\n"
                    found = True
                    continue


            index = line.find(data)

            if index > -1 and found:
                #the request exists!
                requested_data += line + "\r\n"
        if found is False:
            return self.error(data)
        print(requested_data)
        return requested_data + '.'

    def error(self, request):
        '''
        elegantly handles a file or directory not found
        '''
        return "ERROR: "+request+"\nCould not be found!\n"


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

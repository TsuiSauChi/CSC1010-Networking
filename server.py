
from socket import *
from status import Status
from threading import Thread
import os
import struct
import sys


BUFFER_SIZE = 2048

class Threadchild(Thread):
    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.status = Status()
        self.status.setCode("230")
        self.status.setMessage("User logged in")
        print(self.status.getCode() + self.status.getMessage()
                + " from " + ip + ":" + str(port))

    def run(self):
        cmd = self.sock.recv(BUFFER_SIZE).decode()
        if "LIST" in str(cmd):
            self.status.setCode("212")
            self.status.setMessage("Directory status.")
            self.sock.send(self.status.getCode().encode())
            self.listing()
            
        elif "UPLD" in str(cmd):
            self.status.setCode("126")
            self.status.setMessage("Data connection already open; transfer starting.")
            self.sock.send(self.status.getCode().encode())
            self.upload(str(cmd)[4:].strip())

        elif "DWLD" in str(cmd):
            self.status.setCode("125")
            self.status.setMessage("Data connection already open; transfer starting.")
            self.sock.send(self.status.getCode().encode())
            # Removes all the leading as well as trailing spaces 
            self.download(str(cmd)[4:].strip())

        elif "DELF" in str(cmd):
            self.delete(str(cmd)[4:].strip())

        elif "QUIT" in str(cmd):
            self.sock.close()

        return

    def listing(self):
        print("Listing files...")
        # Get list of files in directory
        listing = os.listdir(os.getcwd())
        print(listing)

        self.sock.send(str(len(listing)).encode())
        for item in listing:
            # "i" int for pack 1st param
            self.sock.send(struct.pack("i", sys.getsizeof(item)))
            self.sock.send(item.encode())
            self.sock.recv(1).decode()

        #self.sock.recv(BUFFER_SIZE)
        print("Successfully sent file listing")
        return


    def upload(self, filename):
        f = open(filename, 'wb')
        while True:
            l = self.sock.recv(BUFFER_SIZE)
            while l:
                print('receiving data...')
                f.write(l)
                l = self.sock.recv(BUFFER_SIZE)
            f.close()
            print('file close()')
            #self.sock.shutdown(socket.SHUT_WR)
            self.sock.close()
            break


    def download(self, filename):
        f = open(filename, 'rb')
        l = f.read(BUFFER_SIZE)
        # While not EOF
        while l:
            self.sock.send(l)
            #print('Sent ',repr(l))
            l = f.read(BUFFER_SIZE)
        f.close()
        self.sock.close()

    def delete(self, filename):
        if os.path.isfile(filename):
            print("File exist")
            os.remove(filename)
            self.status.setCode("313")
            self.status.setMessage("File Deleted")
            self.sock.send(self.status.getCode().encode())
        else:
            print("File not found")
            send_data = "File cannot be found"
            self.sock.send(send_data.encode())

# GET Ip address
SERVER = gethostbyname(gethostname())
# Define server port
serverPort = 10047
# Step 1: Creating a TCP Connection 
serverSocket = socket(AF_INET, SOCK_STREAM)
# Step 2: Associate socket with server 
serverSocket.bind((SERVER, serverPort))
threads = []

while True:
    #print(threads)
    serverSocket.listen(5)
    print("Waiting for incoming connections...")
    # second para returns a tuple with ip and port
    connectionSocket, (ip, port) = serverSocket.accept()
    print('Got connection from', ip, port)
    newthread = Threadchild(ip, port, connectionSocket)
    newthread.run()
    threads.append(newthread)
    #print("End of While Loop")
    #print(threads)

# All thread goes into waiting state for termination
for newthread in threads:
    newthread.join()

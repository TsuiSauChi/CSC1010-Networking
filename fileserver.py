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

        # elif "UPLD" in str(cmd):
        elif "DWLD" in str(cmd):
            self.status.setCode("125")
            self.status.setMessage("Data connection already open; transfer starting.")
            self.sock.send(self.status.getCode().encode())
            # Removes all the leading as well as trailing spaces
            self.download(str(cmd)[4:].strip())
        # elif "DELF" in str(cmd):
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

        # self.sock.recv(BUFFER_SIZE)
        print("Successfully sent file listing")
        return

    def download(self, filename):
        f = open(filename, 'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            # While not EOF
            while (l):
                self.sock.send(l)
                # print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break


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
    print(threads)
    # What is 5 here?
    serverSocket.listen(5)
    print("Waiting for incoming connections...")
    # second para returns a tuple with ip and port
    connectionSocket, (ip, port) = serverSocket.accept()
    print('Got connection from', ip, port)
    newthread = Threadchild(ip, port, connectionSocket)
    newthread.run()
    threads.append(newthread)
    print("End of While Loop")
    print(threads)

# All thread goes into waiting state for termination
for newthread in threads:
    newthread.join()

'''
while True:
    tcpsock.listen(5)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got connection from ', (ip,port)
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()



import os
import socket 
print(os.listdir(os.getcwd()))

# REFERENCE CODE 
eif data == "LIST":
        list_files()

def list_files():
    print "Listing files..."
    # Get list of files in directory
    listing = os.listdir(os.getcwd())
    # Send over the number of files, so the client knows what to expect (and avoid some errors)
    conn.send(struct.pack("i", len(listing)))
    total_directory_size = 0
    # Send over the file names and sizes whilst totaling the directory size
    for i in listing:
        # File name size
        conn.send(struct.pack("i", sys.getsizeof(i)))
        # File name
        conn.send(i)
        # File content size
        conn.send(struct.pack("i", os.path.getsize(i)))
        total_directory_size += os.path.getsize(i)
        # Make sure that the client and server are syncronised
        conn.recv(BUFFER_SIZE)
    # Sum of file sizes in directory
    conn.send(struct.pack("i", total_directory_size))
    #Final check
    conn.recv(BUFFER_SIZE)
    print "Successfully sent file listing"
    return
'''

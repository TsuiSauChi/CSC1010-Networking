from socket import *
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

    def run(self):
        cmd = self.sock.recv(BUFFER_SIZE).decode()

        if "D" in str(cmd):
            # Removes all the leading as well as trailing spaces
            self.download()
        elif "U" in str(cmd):
            self.upload()

        return

    def download(self):
        f = open("database.db", 'rb')
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

    def upload(self):
        pass


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
    # What is 5 here?
    serverSocket.listen(5)
    print("Waiting for incoming connections...")
    # second para returns a tuple with ip and port
    connectionSocket, (ip, port) = serverSocket.accept()
    print('Got connection from', ip, port)
    newthread = Threadchild(ip, port, connectionSocket)
    newthread.run()
    threads.append(newthread)

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

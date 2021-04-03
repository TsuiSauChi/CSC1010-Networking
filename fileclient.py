import socket
import sys
import struct

# GET IP address
SERVER = socket.gethostbyname(socket.gethostname())
serverPort = 10047

# Step 1: Create a TCP/IP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Connect the socket to the port where the server is listening
print(f'connecting to {SERVER} port {serverPort}')
clientSocket.connect((SERVER, serverPort))

def download():
    # Run program
    try:

            cmd = "D".encode()
            print("Sending cmd", cmd)
            clientSocket.send(cmd)

            bufferSize = 2048

            with open('database.db', 'wb') as f:
                print('file opened')
                while True:
                    print('receiving data...')
                    data = clientSocket.recv(2048)
                    print(f'data = {data}')
                    if not data:
                        f.close()
                        print('file close()')
                        break
                    # write data to a file
                    f.write(data)

    finally:

        clientSocket.close()

download()

# REFERENCE CODE
'''
def list_files():
    # List the files avaliable on the file server
    # Called list_files(), not list() (as in the format of the others) to avoid the standard python function list()
    print "Requesting files...\n"
    try:
        # Send list request
        s.send("LIST")
    except:
        print "Couldn't make server request. Make sure a connection has bene established."
        return
    try:
        # First get the number of files in the directory
        number_of_files = struct.unpack("i", s.recv(4))[0]
        # Then enter into a loop to recieve details of each, one by one
        for i in range(int(number_of_files)):
            # Get the file name size first to slightly lessen amount transferred over socket
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size)
            # Also get the file size for each item in the server
            file_size = struct.unpack("i", s.recv(4))[0]
            print "\t{} - {}b".format(file_name, file_size)
            # Make sure that the client and server are syncronised
            s.send("1")
        # Get total size of directory
        total_directory_size = struct.unpack("i", s.recv(4))[0]
        print "Total directory size: {}b".format(total_directory_size)
    except:
        print "Couldn't retrieve listing"
        return
    try:
        # Final check
        s.send("1")
        return
    except:
        print "Couldn't get final server confirmation"
        return
'''

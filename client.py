import socket
from status import Status
import sys
import struct

#GET IP address
SERVER = socket.gethostbyname(socket.gethostname())
serverPort = 10047

# Step 1: Create a TCP/IP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
status = Status()

# Step 2: Connect the socket to the port where the server is listening
print(f'connecting to {SERVER} port {serverPort}')
clientSocket.connect((SERVER, serverPort))

# Run program
try:

    cmd = ""

    while True:

        print("Welcome to the FTP client.")
        print("Please input one of the following commands to execute:")
        print("UPLD file_path : Upload file")
        print("LIST           : List files")
        print("DWLD file_path : Download file")
        print("DELF file_path : Delete file")
        print("QUIT           : Exit")

        cmd = input("\nEnter a command: ")

        #Check if file path was specified
        if "UPLD" in cmd or "DWLD" in cmd or "DELF" in cmd:
            if len(cmd) <= 5:
                status.setCode("501")
                status.setMessage("Syntax error in parameters or arguments; Missing file path.")
                print(status.getCode(), status.getMessage())
                continue

        # If client quitting, send message and then end on client's side
        if "QUIT" in cmd:
            break

        # Step 3: To send message to server 
        cmd = cmd.encode()
        print("Sending cmd", cmd)
        clientSocket.send(cmd)

        # Step 4: To receive data from server
        bufferSize = 2048
        reply = clientSocket.recv(bufferSize).decode()
        print(reply)

        #Downloading files
        if reply == "125":
            status.setCode("250")
            status.setMessage("Requested file action okay, completed.")
            print(status.getCode(), status.getMessage())
            with open('received_file', 'wb') as f:
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
        #Listing files
        elif reply == '212':
            try:
                # First get the number of files in the directory
                # recv(4) is for int byte size
                number_of_files = clientSocket.recv(bufferSize).decode()
                print(number_of_files)
                # Then enter into a loop to recieve details of each, one by one
                for _ in range(int(number_of_files)):
                    file_name_size = struct.unpack("i", clientSocket.recv(4))[0]
                    file_name = clientSocket.recv(file_name_size).decode()
                    print(file_name)
                    clientSocket.send("1".encode()) 
            except:
                print("Couldn't retrieve listing")

finally:
    
    status.setCode("226")
    status.setMessage("Closing data connection. Request successful.")
    print(status.getCode(), status.getMessage())
    clientSocket.close()


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

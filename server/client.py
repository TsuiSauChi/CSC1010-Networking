import socket
from status import Status
import sys
import struct

# Run program
try:

    while True:

        # GET IP address
        SERVER = socket.gethostbyname(socket.gethostname())
        serverPort = 10047

        # Step 1: Create a TCP/IP socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        status = Status()

        # Step 2: Connect the socket to the port where the server is listening
        print(f'connecting to {SERVER} port {serverPort}')
        clientSocket.connect((SERVER, serverPort))

        #cmd = ""

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
        elif "QUIT" in cmd:
            break

        else:
            continue # Refuse any other input

        # Step 3: To send message to server
        filename = str(cmd)[4:].strip()
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
            f = open(filename, 'wb')
            while True:
                l = clientSocket.recv(bufferSize)
                while l:
                    #if not l:
                    #    f.close()
                    #    print('file close()')
                    #    break
                    print('receiving data...')
                    f.write(l)
                    l = clientSocket.recv(bufferSize)
                f.close()
                print('file close()')
                clientSocket.shutdown(socket.SHUT_WR)
                clientSocket.close()
                break

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

        # Uploading file
        elif reply == "126":
            f = open(filename, 'rb')
            l = f.read(bufferSize)
            # While not EOF
            while l:
                clientSocket.send(l)
                # print('Sent ',repr(l))
                l = f.read(bufferSize)
            f.close()
            clientSocket.close()

        # Deleting files
        elif reply == "313":
            status.setCode("260")
            status.setMessage("File deleted")
            print(status.getCode(), status.getMessage())

finally:

    status.setCode("226")
    status.setMessage("Closing data connection. Request successful.")
    print(status.getCode(), status.getMessage())
    clientSocket.close()

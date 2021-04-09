import socket
from status import Status
import sys
import struct
import os

# Run program
try:

    while True:

        # GET IP address
        SERVER = socket.gethostbyname(socket.gethostname())
        serverPort = 10065

        # Step 1: Create a TCP/IP socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        status = Status()

        # Step 2: Connect the socket to the port where the server is listening
        print(f'Connecting to {SERVER} port {serverPort}')
        clientSocket.connect((SERVER, serverPort))

        print("Welcome to the FTP client.")
        print("Please input one of the following commands to execute:")
        print("UPLD file_path : Upload file")
        print("LIST           : List files")
        print("DWLD file_path : Download file")
        print("DELF file_path : Delete file")
        print("QUIT           : Exit")

        cmd = input("\nEnter a command: ")
        print()

        #Check if file path was specified
        if "UPLD" in cmd or "DWLD" in cmd or "DELF" in cmd:
            if len(cmd) <= 5:
                status.setCode("501")
                status.setMessage("Syntax error in parameters or arguments; Missing file path.")
                print("ERROR", status.getCode(), status.getMessage())
                print()
                continue
            
            if "UPLD" in cmd:
                filename = str(cmd)[4:].strip()
                if not os.path.isfile(filename):
                    status.setCode("550")
                    status.setMessage("Requested action not taken. File not found.")
                    print("ERROR", status.getCode(), status.getMessage())
                    print()
                    continue

        # If client quitting, send message and then end on client's side
        elif "QUIT" in cmd:
            break

        else:
            if "LIST" not in cmd: # Refuse any other input
                status.setCode("500")
                status.setMessage("Syntax error, command unrecognized.")
                print("ERROR", status.getCode(), status.getMessage())
                print()
                continue 

        # Step 3: To send message to server
        filename = str(cmd)[4:].strip()
        cmd = cmd.encode()
        #print("Sending cmd", cmd)
        clientSocket.send(cmd)

        # Step 4: To receive data from server
        bufferSize = 2048
        reply = clientSocket.recv(bufferSize).decode()
        #print(reply)

        #Downloading files
        if reply == "125":
            print("Downloading files...\n")
            f = open(filename, 'wb')
            while True:
                l = clientSocket.recv(bufferSize)
                while l:
                    #if not l:
                    #    f.close()
                    #    print('file close()')
                    #    break
                    print("Receiving data...\n")
                    f.write(l)
                    l = clientSocket.recv(bufferSize)
                f.close()
                status.setCode("250")
                status.setMessage("Requested file action okay, completed.")
                print(status.getCode(), status.getMessage())
                clientSocket.shutdown(socket.SHUT_WR)
                clientSocket.close()
                break

        #Listing files
        elif reply == '212':
            print("---START---")
            print("Listing Files: ")
            while True:
                try:
                    data = clientSocket.recv(bufferSize)
                    if len(data) == 0: # Connection close
                        break
                    print(data.decode('ascii').strip())
                except (socket.error): # Connection closed
                    break
            print("---END---")
            clientSocket.close()

        # Uploading file
        elif reply == "126":
            f = open(filename, 'rb')
            l = f.read(bufferSize)
            print("Uploading file...\n")
            # While not EOF
            while l:
                clientSocket.send(l)
                # print('Sent ',repr(l))
                l = f.read(bufferSize)
            f.close()
            status.setCode("250")
            status.setMessage("Requested file action okay, completed.")
            print(status.getCode(), status.getMessage())
            clientSocket.close()

        # Deleting files
        elif reply == "313":
            status.setCode("250")
            status.setMessage("Requested file action okay, completed.")
            print(status.getCode(), status.getMessage())
            clientSocket.close()

        # Downloading non existent fie
        elif reply == "550":
            status.setCode("550")
            status.setMessage("Requested action not taken. File not found.")
            print("ERROR", status.getCode(), status.getMessage())
            clientSocket.close()

        print()

finally:

    status.setCode("226")
    status.setMessage("Closing data connection. Request successful.")
    print(status.getCode(), status.getMessage())
    clientSocket.close()

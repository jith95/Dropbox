#server.py

import socket
import time
import os
import sys
import traceback
from threading import Thread
import select









def menu():
    d = {}
    with open(r"Users.txt") as f:
    #with open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt") as f:
        for line in f:
           (key, val) = line.split()
           d[key] = val
    def listfile():
        pass
    def uploadfile():
        pass
    def downloadfile():
        pass
    def deletefile():
        pass
    def sharefile():
        pass
    def showlog():
        pass
    def signup():
        s=1
        while s:
            username  = input("Enter a username:")
            s=0
            for i in d:
                    if i==username:
                        print("Username already exists! Choose a new one")
                        s=1
        while True:
            password  = getpass.getpass("Enter a password:")
            password2 = getpass.getpass("Confirm password:")
            if password == password2:
                #file = open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt", "a+")
                file = open(r"Users.txt", "a+")
                file.write(username+" "+password+"\n")
                file.close()
                break
            print("Passwords don't match!")
    def login():
        s=0
        while True:
            username = input("Login:")
            password = input("Password:")
            #file = open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt", "r")
            file = open(r"Users.txt", "r")
            for i in d:
                if i==username and d[i]==password:
                    s=1
                    break
            if s==1:
                break    
            else:
                print("Incorrect Password!")
                

    print("Welcome...")
    while 1:
        welcome = int(input("1.Sign up\n2.Sign in\nEnter your choice(1-2): "))
        if welcome == 1:
            signup()
            break
        if welcome == 2:
            login()
            break
        if welcome>2 or welcome<1:
            print("Incorrect Choice")
    while 1:
        print("\n1.List files:")
        print("\n2.Upload files:")
        print("\n3.Download files:")
        print("\n4.Delete files:")
        print("\n5.Share files:")
        print("\n6.Show log:")
        print("\n7.Sign out:")
        choice=int(input("Enter choice(1-7): "))
        if(choice==1):
            listfile()
        if(choice==2):
            uploadfile()
        if(choice==3):
            downloadfile()
        if(choice==4):
            deletefile()
        if(choice==5):
            sharefile()
        if(choice==6):
            showlog()
        if(choice==7):
            print("Thank you")
            return 'quit'
        if(choice>7 or choice<1):
            print("Incorrect choice")









# Thread for every new clinet
def client_thread(connection, ip, port, max_buffer_size = 5120):
    clientActive = True

    while clientActive:
        menu()
        client_input = receive_input(connection, max_buffer_size)

        # print ("Client Input : " , client_input)

        if client_input.lower() == 'quit':
            print("Client is requesting to quit")
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            clientActive = False
        else:
            print("Processed result: {}".format(client_input))
            connection.sendall("-".encode("utf8"))


# Parses the input received from client
def receive_input(connection, max_buffer_size):
    clientInput = connection.recv(max_buffer_size)
    clientInputSize = sys.getsizeof(clientInput)

    if clientInputSize > max_buffer_size:
        print("The input size is greater than expected " + format(clientInputSize))

    decoded_input = clientInput.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result

# Processes the input received from client
def process_input(input_str):
    print("Processing the input received from client")
    return str(input_str)






# MAIN PROGRAM


serverSockets = []

#socket data object
serverDataSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverDataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
# host = socket.gethostname()
host = ''
port = 5555
#bind to the port
serverDataSocket.bind((host, port))
serverDataSocket.listen(4)
serverSockets.append(serverDataSocket)


#socket command object
serverCmdSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverCmdSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 5556
serverCmdSocket.bind((host, port))
serverCmdSocket.listen(4)
serverSockets.append(serverCmdSocket)


while True:
    # Wait for any sockets to get a hook
    readable, _, _ = select.select(serverSockets, [], [])
    ready_server = readable[0]

    # establish connection
    clientSocket, addr = ready_server.accept()
    ip, port = str(addr[0]), str(addr[1])
    workingPort = ready_server.getsockname()[1]

    print ("Got a connection from : ", str(addr))
    message = "Connected :: "
    currentTime = time.ctime(time.time()) + "\n"

    message += currentTime
    clientSocket.send(message.encode("utf8"))

    try:
        Thread(target=client_thread, args=(clientSocket, ip, port)).start()
    except:
        print("Thread error")
        traceback.print_exc()

    # clientSocket.close()
#server.py

import socket
import time
import os
import sys
import traceback
from threading import Thread
import select


def makeFolder(username):
    if not os.path.exists(username):
        print ("new folder for new user ---- OASIS success")
        os.makedirs(username)

def listfile(connection,username):
    path=os.getcwd()+'\\'+username
    templist = os.listdir(path)
    toBePrinted=''
    for i in templist:
        toBePrinted = toBePrinted+'\n'+i
    connection.sendall(toBePrinted.encode("utf8"))

def uploadfile():
    pass

def downloadfile():
    pass

def deletefile(connection,max_buffer_size,username):
    listfile(connection,username)
    toBePrinted = "Enter file to be deleted: "
    connection.sendall(toBePrinted.encode("utf8"))
    filename = receive_input(connection, max_buffer_size)
    path=os.getcwd()
    if os.name == 'nt':
        r= path+'\\'+username+'\\'+filename
    else:
        r= path+'/'+username+'/'+filename
    if os.path.exists(r):
        os.remove(r)
        toBePrinted = filename + " Has been deleted"
        connection.sendall(toBePrinted.encode("utf8"))
    else:
        toBePrinted = "File doen't exist "
        connection.sendall(toBePrinted.encode("utf8"))

def sharefile():
    pass
def showlog():
    pass




def signup(connection, max_buffer_size):
    s=1
    username = ''
    while s:
        toBePrinted = "Enter a username: "
        connection.sendall(toBePrinted.encode("utf8"))
        username = receive_input(connection, max_buffer_size)        
        s=0
        for i in d:
                if i==username:
                    toBePrinted = "Username already exists! Choose a new one "
                    connection.sendall(toBePrinted.encode("utf8"))
                    s=1
                    break
    while True:

        toBePrinted = "Enter a password: "
        connection.sendall(toBePrinted.encode("utf8"))
        password = receive_input(connection, max_buffer_size)

        toBePrinted = "Confirm password: "
        connection.sendall(toBePrinted.encode("utf8"))
        password2 = receive_input(connection, max_buffer_size) 

        if password == password2:
            d[username]=password  
            makeFolder(username)          
            break
        toBePrinted = "Passwords don't match "
        connection.sendall(toBePrinted.encode("utf8"))


    return username

def login(connection, max_buffer_size):
    s=0
    while True:

        toBePrinted = "Enter userid: "
        connection.sendall(toBePrinted.encode("utf8"))
        username = receive_input(connection, max_buffer_size) 

        toBePrinted = "Enter password: "
        connection.sendall(toBePrinted.encode("utf8"))
        password = receive_input(connection, max_buffer_size)

        for i in d:
            if i==username and d[i]==password:
                s=1
                break
        if s==1:
            break    
        else:
            toBePrinted = "The userid password combination doesn't match "
            connection.sendall(toBePrinted.encode("utf8"))
                
    return username




def menu(connection, max_buffer_size):
   
    toBePrinted = "Welcome...\n1.Sign up\n2.Sign in\nEnter your choice(1-2): "

    while 1:
        connection.sendall(toBePrinted.encode("utf8"))
        client_input = int(receive_input(connection, max_buffer_size))
        if client_input == 1:
            username=signup(connection, max_buffer_size)
            break
        if client_input == 2:
            username=login(connection, max_buffer_size)
            break
        if client_input>2 or client_input<1:
            toBePrinted = "Incorrect Choice"
            connection.sendall(toBePrinted.encode("utf8"))

    while 1:
        toBePrinted = "\n1.List files:\n2.Upload Files:\n3.Download files:\n4.Delete files:\n5.Share files:\n6.Show log:\n7.Sign out:\nEnter choice(1-7): "
        connection.sendall(toBePrinted.encode("utf8"))
        choice = int(receive_input(connection, max_buffer_size))

        if(choice==1):
            listfile(connection,username)
        if(choice==2):
            uploadfile()
        if(choice==3):
            downloadfile()
        if(choice==4):
            deletefile(connection,max_buffer_size,username)
        if(choice==5):
            sharefile()
        if(choice==6):
            showlog()
        if(choice==7):
            toBePrinted = "quit"
            connection.sendall(toBePrinted.encode("utf8"))
            return 'quit'
        if(choice>7 or choice<1):
            toBePrinted = "Incorrect Choice \n"
            connection.sendall(toBePrinted.encode("utf8"))








# Thread for every new clinet
def client_thread(connection, ip, port, max_buffer_size = 5120):
    # clientActive = True
    # client_input = menu(connection, max_buffer_size)

    # while clientActive:
        # client_input = receive_input(connection, max_buffer_size)

        # if client_input.lower() == 'quit':
        #     print("Client is requesting to quit")
        #     connection.close()
        #     print("Connection " + ip + ":" + port + " closed")
        #     clientActive = False
        # else:
        #     print("Processed result: {}".format(client_input))
        #     connection.sendall("-".encode("utf8"))    

    menu(connection, max_buffer_size)
    print("Client is requesting to quit")
    connection.close()
    print("Connection " + ip + ":" + port + " closed")

    # dump the dictionary into the file

    file = open(r"Users.txt", "w+")
    for key, val in d.items():
        file.write(key+" "+val+"\n")
    file.close()




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


#setting up a dictionary from users.txt

d = {}
with open(r"Users.txt") as f:
#with open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt") as f:
    for line in f:
       (key, val) = line.split()
       d[key] = val


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
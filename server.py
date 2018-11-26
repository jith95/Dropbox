#server.py

import socket
import time
import os
import sys
import traceback
from threading import Thread
import select
from datetime import datetime

def updateLogFile(filename,username,action,ip):
    path=os.getcwd()
    if os.name == 'nt':
        r= path+'\\'+'Logs'+'\\'+username+'.txt'
    else:
        r= path+'/'+'Logs'+'/'+username+'.txt'
    file=open(r,'a+')
    s = filename + " " + username + " " + action + " " + ip + " " + str(datetime.now()) + "\n" 
    file.write(s)
    file.close()

def makeLogFile(username):
    path=os.getcwd()
    if os.name == 'nt':
        r= path+'\\'+'Logs'+'\\'+username+'.txt'
    else:
        r= path+'/'+'Logs'+'/'+username+'.txt'
    file=open(r,'a+')
    file.close()

def makeFolder(username):
    if not os.path.exists(username):
        print ("new folder for new user ---- OASIS success")
        os.makedirs(username)

def listfile(connection,username, extraString = ''):
    if os.name=='nt':
        path=os.getcwd()+'\\'+username
    else:
        path = os.getcwd() + '/' + username
    templist = os.listdir(path)
    toBePrinted=''
    for i in templist:
        toBePrinted = toBePrinted+'\n'+i
    toBePrinted += '\n\n' + extraString
    connection.sendall(toBePrinted.encode("utf8"))



def uploadfile(connectionComamnd, connectionData, max_buffer_size, username, ip):
    action = "upload"

    toBePrinted = "Enter filename (complete path if not in CWD): "
    connectionComamnd.sendall(toBePrinted.encode("utf8"))    

    fileSizeAndFileName = receive_input(connectionComamnd, max_buffer_size)

    fileSizeNameList = fileSizeAndFileName.split(':', 1)
    # fileSize is str type

    # Send OK to indicate ready to receive
    connectionComamnd.send('File Size OK'.encode("utf8"))

    fileSizeNameList[1] = fileSizeNameList[1].replace('\\','/')

    fileName = os.path.basename(fileSizeNameList[1])
    print("File size and fileName ", fileSizeNameList[0], fileName)

    currentPath=os.getcwd()
    if os.name == 'nt':
        r= currentPath+'\\'+username+'\\'+fileName
    else:
        r= currentPath+'/'+username+'/'+fileName
    f = open(r, 'wb')

    data = connectionData.recv(1024)
    receivedSize = len(data)
    f.write(data)

    print ("receiving .", end = '')
    sys.stdout.flush()

    printStatus = int(int(fileSizeNameList[0])/10)

    while receivedSize < int(fileSizeNameList[0]):
        
        if (receivedSize % printStatus == 0):
            print (".", end = '')
            sys.stdout.flush()

        data = connectionData.recv(1024)
        receivedSize += len(data)
        f.write(data)
    f.close()
    updateLogFile(fileName,username,action,ip)
    print ("\nFile uploaded successfully")



def downloadfile(connectionCommand, connectionData, username, ip, max_buffer_size):
    toBePrinted = "Enter  the name of the file you want to download : "       
    listfile(connectionCommand,username,toBePrinted)
    filename = receive_input(connectionCommand, max_buffer_size) 

    if os=='nt':
        filePath=os.getcwd()+'\\'+username+'\\'+filename
    else:
        filePath=os.getcwd()+'/'+username+'/'+filename

    fileSizeAndFileName = str(os.path.getsize(filePath))
    fileSizeAndFileName += ":"
    #sendFileName also in same string
    fileSizeAndFileName += filePath

    print("File size and File name: ",fileSizeAndFileName)
    connectionCommand.send(fileSizeAndFileName.encode("utf8"))

    status = receive_input(connectionCommand,max_buffer_size)

    if status == 'File Size OK':
        with open(filePath, 'rb') as f:
            data = f.read(1024)
            connectionData.send(data)
            print ("sending .", end = '')
            sys.stdout.flush()

            printStatus = int(int(fileSizeNameList[0])/10)

            while len(data) != 0:
                if (len(data) % printStatus == 0):
                    print (".", end = '')
                    sys.stdout.flush()

                data = f.read(1024)
                connectionData.send(data)    

    action="download"
    updateLogFile(filename,username,action,ip)
    print ("\nFile downloaded successfully")


def deletefile(connection,max_buffer_size,username,ip):
    extraString = "Enter file to be deleted: "
    listfile(connection,username, extraString)
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
    action="delete"
    updateLogFile(filename,username,action,ip)    

def sharefile(connection,username,ip,max_buffer_size):
    extraString = "Enter file to be shared: "
    listfile(connection,username, extraString)
    filename = receive_input(connection, max_buffer_size)

    path=os.getcwd()
    if os.name == 'nt':
        source= path+'\\'+username+'\\'+filename
    else:
        source= path+'/'+username+'/'+filename

    toBePrinted = "Enter user you want to share it with: "
    connection.sendall(toBePrinted.encode("utf8"))
    path2 = receive_input(connection, max_buffer_size)

    if os.name == 'nt':
        dest= path+'\\'+path2+'\\'+filename
    else:
        dest= path+'/'+path2+'/'+filename

    os.symlink(source,dest)
    action="share"
    updateLogFile(filename,username,action,ip)

    toBePrinted = "File shared successfully"
    connection.sendall(toBePrinted.encode("utf8"))

def showlog(connection,username):
    path=os.getcwd()
    if os.name == 'nt':
        r= path+'\\'+'Logs'+'\\'+username+'.txt'
    else:
        r= path+'/'+'Logs'+'/'+username+'.txt'
    toBePrinted = "USER FILE ACTION IP DATE  \n" 
    file=open(r,'r')
    for i in file:
        toBePrinted = toBePrinted + i
    connection.sendall(toBePrinted.encode("utf8"))
    file.close()




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
            makeLogFile(username)         
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




def menu(connectionCommand, connectionData, max_buffer_size,ip):
   
    toBePrinted = "Welcome...\n1.Sign up\n2.Sign in\nEnter your choice(1-2): "

    while 1:
        connectionCommand.sendall(toBePrinted.encode("utf8"))
        client_input = int(receive_input(connectionCommand, max_buffer_size))
        if client_input == 1:
            username=signup(connectionCommand, max_buffer_size)
            break
        if client_input == 2:
            username=login(connectionCommand, max_buffer_size)
            break
        if client_input>2 or client_input<1:
            toBePrinted = "Incorrect Choice"
            connectionCommand.sendall(toBePrinted.encode("utf8"))

    while 1:
        toBePrinted = "\n1.List files:\n2.Upload Files:\n3.Download files:\n4.Delete files:\n5.Share files:\n6.Show log:\n7.Sign out:\nEnter choice(1-7): "
        connectionCommand.sendall(toBePrinted.encode("utf8"))
        choice = int(receive_input(connectionCommand, max_buffer_size))

        if(choice==1):
            listfile(connectionCommand,username)
        if(choice==2):
            uploadfile(connectionCommand, connectionData, max_buffer_size,username,ip)
        if(choice==3):
            downloadfile(connectionCommand, connectionData, username,ip,max_buffer_size)
        if(choice==4):
            deletefile(connectionCommand,max_buffer_size,username,ip)
        if(choice==5):
            sharefile(connectionCommand,username,ip,max_buffer_size)
        if(choice==6):
            showlog(connectionCommand,username)
        if(choice==7):
            toBePrinted = "quit"
            connectionCommand.sendall(toBePrinted.encode("utf8"))
            return 'quit'
        if(choice>7 or choice<1):
            toBePrinted = "Incorrect Choice \n"
            connectionCommand.sendall(toBePrinted.encode("utf8"))








# Thread for every new clinet
def client_thread(connectionCommand, connectionData, ip, port, max_buffer_size = 5120):
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

    menu(connectionCommand, connectionData,  max_buffer_size,ip)
    print("Client is requesting to quit")
    connectionCommand.close()
    connectionData.close()
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

# Make a folder for Logs
makeFolder('Logs')

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

ipToSocketsDictionary = {}

while True:
    # Wait for any sockets to get a hook
    readable, _, _ = select.select(serverSockets, [], [])
    ready_server = readable[0]

    # establish connection
    socketConnect, addr = ready_server.accept()
    # dataSocket, addr2 = ready_server.accept()
    ip, port = str(addr[0]), str(addr[1])
    # workingPort = ready_server.getsockname()[1]

    if ip in ipToSocketsDictionary:
        ipToSocketsDictionary[ip].append(socketConnect)
    else:
        ipToSocketsDictionary[ip] = [socketConnect]
        continue

    print ("Got a connection from : ", str(addr))
    message = "Connected :: "
    currentTime = time.ctime(time.time()) + "\n"

    message += currentTime
    ipToSocketsDictionary[ip][0].send(message.encode("utf8"))

    print ("ipToSocketsDictionary : ", ipToSocketsDictionary)

    try:
        # First hook will always be on command socket and then on dataSocket
        Thread(target=client_thread, args=(ipToSocketsDictionary[ip][0], ipToSocketsDictionary[ip][1], ip, port)).start()
    except:
        print("Thread error")
        traceback.print_exc()

    #Clear ipToDic here itself, as more clients to connect from same PC
    ipToSocketsDictionary.pop(ip, None)    

    # clientSocket.close()
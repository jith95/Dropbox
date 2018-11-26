#client.py

import socket
import sys
import getpass
import os

def  downloadFileClient(connectionComamnd, connectionData, filePath):

    connectionComamnd.sendall(filePath.encode("utf8"))
    fileSizeAndFileName = connectionComamnd.recv(1024).decode("utf8")

    fileSizeNameList = fileSizeAndFileName.split(':', 1)
    # fileSize is str type
    # Send OK to indicate ready to receive
    connectionComamnd.send('File Size OK'.encode("utf8"))

    fileSizeNameList[1] = fileSizeNameList[1].replace('\\','/')

    filename = os.path.basename(fileSizeNameList[1])
    print("File size and fileName ", fileSizeNameList[0], filename)
    currentPath=os.getcwd()

    if os=='nt':
        filePath=currentPath+'\\'+filename
    else:
        filePath=currentPath+'/'+filename

    f = open(filePath, 'wb')

    data = connectionData.recv(1024)
    receivedSize = len(data)
    f.write(data)

    while receivedSize < int(fileSizeNameList[0]):
        data = connectionData.recv(1024)
        receivedSize += len(data)
        f.write(data)
    f.close()
    print(" File downloaded successfully. Return to main menu:")

def uploadFileClient(connectionComamnd, connectionData, filePath):

    fileSizeAndFileName = str(os.path.getsize(filePath))
    fileSizeAndFileName += ":"
    #sendFileName also in same string
    fileSizeAndFileName += filePath
    # send file size
    print("fileSize and fileName: ", fileSizeAndFileName)
    connectionComamnd.send(fileSizeAndFileName.encode("utf8"))

    status = connectionComamnd.recv(1024).decode("utf8")
    if status == 'File Size OK':
        with open(filePath, 'rb') as f:
            data = f.read(1024)
            connectionData.send(data)
            
            while len(data) != 0:
                data = f.read(1024)
                connectionData.send(data)
    print ("File uploaded successfully. Return to main menu:")

def clientConnect(hostStr, dataPort, cmdPort):

    #create socket object
    commandSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    dataSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = hostStr
    # Connecting to cmdPort first
    port = cmdPort
    try:
        commandSocket.connect((host, port))
    except:
        print("Connection error : Command Socket")
        sys.exit()  

    port = dataPort
    try:
        dataSocket.connect((host, port))
    except:
        print("Connection error : Data Socket")
        sys.exit()

    print("Enter 'quit' to exit")

    #Receive 5120B of data
    tm = commandSocket.recv(5120)
    print (tm.decode("utf8"))

    toBePrinted = ''
    message = ''
    #use getpass function for entering a password



    while message != 'quit':
        toBePrinted = commandSocket.recv(5120).decode("utf8")
        if (toBePrinted.lower() == 'quit'):
            break

        print(toBePrinted)

        if (toBePrinted == "Enter a password: " or 
        toBePrinted == "Confirm password: " or
        toBePrinted == "Enter password: "):
            message = getpass.getpass(prompt='')
            commandSocket.sendall(message.encode("utf8"))

        elif (toBePrinted == "Enter filename (complete path if not in CWD): "):
            message = input()
            uploadFileClient(commandSocket, dataSocket, message)

        elif "Enter  the name of the file you want to download : " in toBePrinted:
            message = input()
            downloadFileClient(commandSocket, dataSocket, message)

        else:
            message = input()
            commandSocket.sendall(message.encode("utf8"))
       
    commandSocket.close()
    dataSocket.close()





# Main Function
print ("\n\n<<<<<<<<<<<<< Welcome to OASIS >>>>>>>>>>>>>\n\n")
dataPort= input("Enter dataPort : ")
cmdPort = input("Enter commandPort : ")
clientConnect(sys.argv[1], int(dataPort), int(cmdPort))

#python client.py 10.1.130.250
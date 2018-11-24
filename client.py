#client.py

import socket
import sys
import getpass


def clientConnect(hostStr, dataPort, cmdPort):

    #create socket object
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = hostStr
    # Connecting to cmdPort first
    port = cmdPort

    try:
        clientSocket.connect((host, port))
    except:
        print("Connection error")
        sys.exit()  

    print("Enter 'quit' to exit")

    #Receive 5120B of data
    tm = clientSocket.recv(5120)
    print (tm.decode("utf8"))

    toBePrinted = ''
    message = ''
    #use getpass function for entering a password



    while message != 'quit':
        toBePrinted = clientSocket.recv(5120).decode("utf8")
        if (toBePrinted.lower() == 'quit'):
        	break

        print(toBePrinted)

        if (toBePrinted == "Enter a password: " or toBePrinted == "Confirm password: " or toBePrinted == "Enter password: "):
            message = getpass.getpass(prompt='')
        else:
            message = input()
        
        clientSocket.sendall(message.encode("utf8"))

    clientSocket.close()





# Main Function
print ("\n\n<<<<<<<<<<<<< Welcome to OASIS >>>>>>>>>>>>>\n\n")
dataPort= input("Enter dataPort : ")
cmdPort = input("Enter commandPort : ")
clientConnect(sys.argv[1], int(dataPort), int(cmdPort))

#python client.py 10.1.130.250
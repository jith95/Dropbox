#client.py

import socket
import sys
def menu():
    d = {}
    with open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt") as f:
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
            password  = input("Enter a password:")
            password2 = input("Confirm password:")
            if password == password2:
                file = open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt", "a+")
                #file = open(r"file.txt", "a+")
                file.write(username+" "+password+"\n")
                file.close()
                break
            print("Passwords don't match!")
    def login():
        s=0
        while True:
            username = input("Login:")
            password = input("Password:")
            file = open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt", "r")
            #file = open(r"file.txt", "r")
            for i in d:
                if i==login1 and d[i]==login2:
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
def clientConnect(hostStr, dataPort, cmdPort):

    #create socket object
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #host address
    # host = '10.1.139.91'

    # port = 5555

    host = hostStr
    # Connecting to cmdPort first
    port = cmdPort

    # clientSocket.connect((host, port))
    try:
        clientSocket.connect((host, port))
    except:
        print("Connection error")
        sys.exit()  

    print("Enter 'quit' to exit")

    #Receive 1024 B of data
    tm = clientSocket.recv(1024)

    print (tm.decode("utf8"))

    message = 's'

    while message.lower() != 'quit':
        clientSocket.sendall(message.encode("utf8"))
        if clientSocket.recv(5120).decode("utf8") == "-":
            pass        # null operation
        message = menu()
    clientSocket.sendall(message.encode("utf-8"))
    clientSocket.close()

print ("\n\n<<<<<<<<<<<<< Welcome to OASIS >>>>>>>>>>>>>\n\n")
dataPort= input("Enter dataPort : ")
cmdPort = input("Enter commandPort : ")
clientConnect('localhost', int(dataPort), int(cmdPort))

#python client.py 10.1.130.250
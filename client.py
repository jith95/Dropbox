#client.py

import socket
import sys

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

	message = input(" -> ")

	while message.lower() != 'quit':
		clientSocket.sendall(message.encode("utf8"))
		if clientSocket.recv(5120).decode("utf8") == "-":
			pass        # null operation

		message = input(" -> ")
	clientSocket.sendall(message.encode("utf-8"))
	clientSocket.close()

print ("\n\n<<<<<<<<<<<<< Welcome to OASIS >>>>>>>>>>>>>\n\n")
dataPort= input("Enter dataPort : ")
cmdPort = input("Enter commandPort : ")
clientConnect(str(sys.argv[1]), int(dataPort), int(cmdPort))

#python client.py 10.1.130.250
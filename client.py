#client.py

import socket
import sys

def clientConnect(hostStr, portStr):

	#create socket object
	clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	#host address
	# host = '10.1.139.91'

	# port = 5555

	host = hostStr
	port = portStr

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
clientConnect('localhost',5555)



#python client.py 10.1.130.250
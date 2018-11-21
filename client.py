#client.py

import socket
import sys

def clientConnect(hostStr, portStr):

	#create socket object
	clientSocket = socket.socket(
		socket.AF_INET,
		socket.SOCK_STREAM)

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

	#Receive 1024 B of data
	tm = clientSocket.recv(1024)
	clientSocket.close()

	print (tm.decode('ascii'))


print ("\n\n<<<<<<<<<<<<< Welcome to OASIS >>>>>>>>>>>>>\n\n")
clientConnect('localhost',5555)



#python client.py 10.1.130.250
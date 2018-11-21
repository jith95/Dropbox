#server.py

import socket
import time
import os
import sys
import traceback
from threading import Thread

# Thread for every new clinet
def client_thread(connection, ip, port, max_buffer_size = 5120):
    clientActive = True

    while clientActive:
        client_input = receive_input(connection, max_buffer_size)
        if "--QUIT--" in client_input:
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
    return "Hello " + str(input_str).upper()






# MAIN PROGRAM

#socket object
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire

# host = socket.gethostname()
host = ''
port = 5555

#bind to the port
serverSocket.bind((host, port))

serverSocket.listen(4)

while True:
	#establish connection
	clientSocket, addr = serverSocket.accept()
	ip, port = str(addr[0]), str(addr[1])

	print ("Got a connection from : ", str(addr))
	message = "Connected :: "
	currentTime = time.ctime(time.time()) + "\n"

	message += currentTime
	clientSocket.send(message.encode('ascii'))

	try:
		Thread(target=client_thread, args=(clientSocket, ip, port)).start()
	except:
		print("Thread error")
		traceback.print_exc()

	clientSocket.close()
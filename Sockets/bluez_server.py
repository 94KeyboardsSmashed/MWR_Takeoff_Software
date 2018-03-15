import bluetooth

ADDRESS = "B8:27:EB:81:20:92"
print(ADDRESS)
PORT = 3

#The backlog argument must be at least 1
#it specifies the number of unaccepted connections 
#that the system will allow before refusing new connections.
BACKLOG = 1

#Receive up to buffersize bytes from the socket
SIZE = 1024

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.bind((ADDRESS, PORT))
sock.listen(BACKLOG)
try:
    client, address = sock.accept()
    while True:
        data = client.recv(SIZE)
        data = data.decode('utf-8')
        print((address[0], data))
except:
    print("Closing Socket")
    client.send("GOODBYE!")
    client.close()
    sock.shutdown(2)
    sock.close()

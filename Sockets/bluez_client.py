import bluetooth
import time

ADDRESS = []
PORT = 3
BACKLOG = 1024

print('Scanning...')
while len(ADDRESS) < 1:
     ADDRESS = bluetooth.discover_devices()
print('Address Found')

def sendData(socket, text):
    socket.sendall(text)
    data = socket.recv(BACKLOG)
    print("SENT: {0: >30} -> RECVD: {1}".format(text, data))

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
for i in ADDRESS:
    try:
        sock.connect((i, PORT))
        break
    except Exception:
        sock.shutdown(2)
        sock.close()
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

sendData(sock, "Hello!")
try:
    while True:
        inp = str(time.time())
        sendData(sock, inp)
except Exception as error:
    sock.shutdown(2)
    sock.close()
    print(error)

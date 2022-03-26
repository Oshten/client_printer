import socket

from settings import STATUS_REQUEST, MAILING_STATUS_REQUEST, PORT


simulator = socket.socket()
simulator.bind(('', PORT))
simulator.listen(1)

client, address = simulator.accept()

ANSWER_STATUS = '^0=RS2 0 0 9 0'
ANSWER_MAILING_STATUS = '^0=SM256 0 0 100000 0'


while True:
    data = client.recv(1024)
    if not data:
        break
    data = data.decode()
    print(data)
    if data == STATUS_REQUEST:
        client.send(ANSWER_STATUS.encode())
    elif data == MAILING_STATUS_REQUEST:
        client.send(ANSWER_MAILING_STATUS.encode())

simulator.close()
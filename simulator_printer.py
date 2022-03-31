import socket

from settings import STATUS_REQUEST, MAILING_STATUS_REQUEST



simulator = socket.socket()
simulator.bind(('', 3000))
simulator.listen(1)

client, address = simulator.accept()

ANSWER_STATUS = '^0=RS2 0 0 9 0'
ANSWER_MAILING_STATUS = '^0=SM256 0 0 50 0'


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

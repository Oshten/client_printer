import re
import time
import socket


HOST = '192.168.177.3'                                          # хост принтера
PORT = 3000                                                 # порт, к которому подключен принтер
QUANTITY_RECORDS = 50

STATUS_REQUEST = '^0?RS<CR>\n\r'
MAILING_STATUS_REQUEST = '^0?SM<CR>\n\r'
REQUEST_FOR_PARAMETER = f'^0=CM{QUANTITY_RECORDS}<CR>\n\r'
TEXT_RECORD = '^0=MR{}\t{}<CR>\n\r'
START_PRINT_OUT = '^0!GO<CR>\n\r'

ERRORS = {
    '1015': 'Буфер заполнен',
    '1018': 'Неверный или отсутствующий номер индекса',
    '1019': 'Непоследовательный номер индекса',
    '5043': 'Буффер пуст',
}

DATA_ARREY = [f'Text {i}' for i in range(1, QUANTITY_RECORDS + 1)]     # массив с данными


client = socket.socket()
client.connect((HOST, PORT))
print('Соединение установлено')

client.send(STATUS_REQUEST.encode(encoding='utf-8'))
answer_status = client.recv(1024).decode(encoding='utf-8')
print(answer_status)
if not re.search(r'.0=RS', answer_status):
    print('Принтер не готов')
    client.close()

client.send(MAILING_STATUS_REQUEST.encode(encoding='utf-8'))
answer_mailing_status = client.recv(1024).decode(encoding='utf-8')
print(answer_mailing_status)
if not re.search(r'.0=SM256', answer_mailing_status):
    print('Принтер не готов к печати')
    client.close()

client.send(REQUEST_FOR_PARAMETER.encode(encoding='utf-8'))
print('На принтер отправлены параметры передачи')

client.send(MAILING_STATUS_REQUEST.encode(encoding='utf-8'))
new_answer_mailing_status = client.recv(1024).decode(encoding='utf-8')
print(new_answer_mailing_status)
parameter_answer = re.search(r'.0=SM256\s\d*\s\d*\s(\d*)\s\d', new_answer_mailing_status)
try:
    if int(parameter_answer[1]) != QUANTITY_RECORDS:
        print('Ошибка! Параметры передачи не установлены')
        client.close()
    print('Параметры передачи установлены')
except TypeError:
    print('Принтер не отвечает')
    client.close()

for i, record in enumerate(DATA_ARREY[:20]):
    client.send(TEXT_RECORD.format(i+1, record).encode(encoding='utf-8'))
    print(f'На принтер отправлена запить: {TEXT_RECORD.format(i+1, record)}')
for _ in range(6):
    client.send(MAILING_STATUS_REQUEST.encode(encoding='utf-8'))
    new_answer_mailing_status = client.recv(1024).decode(encoding='utf-8')
    print(new_answer_mailing_status)
    try:
        quantity_records = re.search(r'.0=SM256\s(\d*)\s\d*\s\d*\s\d', new_answer_mailing_status)[1]
        if int(quantity_records) >= 19:
            print('20 записей загружено')
            break
    except TypeError:
        print('Нестандартный ответ')
    print('Выполняется загрузка для печати. Ожидайте...')
    time.sleep(10)
else:
    print('Произошла ошибка загрузки')
    client.close()

client.send(START_PRINT_OUT.encode(encoding='utf-8'))
print('Начата печать')

next_record = 20
while next_record < 51:
    client.send(STATUS_REQUEST.encode(encoding='utf-8'))
    answer_status = client.recv(1024).decode(encoding='utf-8')
    print(answer_status)

    client.send(MAILING_STATUS_REQUEST.encode(encoding='utf-8'))
    answer_mailing_status = client.recv(1024).decode(encoding='utf-8')
    print(answer_mailing_status)
    try:
        quantity_records = re.search(r'.0=SM256\s(\d*)\s\d*\s\d*\s\d', answer_mailing_status)[1]
    except TypeError:
        quantity_records = 20
        print('Нестандартный ответ')
    if quantity_records >= 19 or next_record == 50 and quantity_records > 0:
        time.sleep(1)
        continue

    print('Отправка 10 новых записей')
    for i, record in enumerate(DATA_ARREY[(next_record):(next_record+10)]):
        print(f'На принтер отправлена запить: {TEXT_RECORD.format(i + 1, record)}')
        client.send(TEXT_RECORD.format(i + 1 + next_record, record).encode(encoding='utf-8'))
    next_record += 10

client.close()


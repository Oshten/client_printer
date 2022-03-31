import time

from settings import HOST, PORT, TEXT_RECORD, START_PRINT_OUT
from function import (
    client,
    request_mailing_status,
    request_all_statuses,
    find_errors,
    find_record_number,
)



DATA_ARREY = [f'Text {i}' for i in range(1, 1001)]     # массив с данными





def main():
    client.connect((HOST, PORT))

    answer_status, answer_mailing_status = request_all_statuses()

    if not answer_status == '^0=RS2 0 0 9 0':
        print('Принтер не готов')
        client.close()
        return
    elif not answer_mailing_status == '^0=SM256 0 0 100000 0':
        print('Принтер не готов к печати')
        client.close()
        return
    for i, record in enumerate(DATA_ARREY[:256]):
        client.send(TEXT_RECORD.format(i+1, record).encode())
    for _ in range(6):
        answer_mailing_status = request_mailing_status()
        if answer_mailing_status == '^0=SM256 255 0 100000 0':
            break
        print('Выполняется загрузка для печати. Ожидайте...')
        time.sleep(10)
    else:
        # перед закрытием соединения я бы отправил команду на очистку буфера памяти, но в инструкции такая команда не представлена
        print('Произошла ошибка загрузки')
        client.close()
        return
    client.send(START_PRINT_OUT.encode())

next_record = 256
while next_record < 1002:
    answer_status, answer_mailing_status = request_all_statuses()
    print(find_errors(answer_status))
    buffer_full, qyentity_pages = find_record_number(answer_mailing_status)
    if buffer_full > 206 or qyentity_pages:
        time.sleep(1)
        continue
    for i, record in enumerate(DATA_ARREY[(next_record):(next_record+50)]):
        client.send(TEXT_RECORD.format(i + 1 + next_record, record).encode())
    next_record += 50
    if next_record > 1001:
        next_record = 1001

client.close()

if __name__ == '__main__':
    main()




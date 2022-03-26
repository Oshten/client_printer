import re
import socket

from settings import STATUS_REQUEST, MAILING_STATUS_REQUEST, ERRORS



client = socket.socket()

def request_status():
    '''Запрос статуса принтера и получение ответа'''
    client.send(STATUS_REQUEST.encode())
    answer_status = client.recv(1024).decode()
    return answer_status

def request_mailing_status():
    '''Запрос статуса рассылки и получение ответа'''
    client.send(MAILING_STATUS_REQUEST.encode())
    answer_mailing_status = client.recv(1024).decode()
    return answer_mailing_status

def request_all_statuses():
    '''Запрос статусов принтера и рассылки и получение ответов'''
    answer_status = request_status()
    answer_mailing_status = request_mailing_status()
    return answer_status, answer_mailing_status

def find_errors(answer_status):
    '''Поиск ошибок в статусе принтера'''
    try:
        error_number = re.search(r'.0=RS2 6 (\d{4}) 9 0', answer_status)[1]
        error = ERRORS.get(error_number, 'Неизвестная ошибка') # сообщение "Неизвестная ошибка" удалить когда в ERRORS будет внесен полный список ошибок
        return f'Ошибка {error_number}: {error}'
    except TypeError:
        return 'Ошибок нет'


def find_record_number(answer_mailing_status):
    '''Поиск номера напечатанной страницы'''
    try:
        search_answer = re.search(r'.0=SM256 (\d{1,3}) (\d{1,4}) 100000 \d{1,4}', answer_mailing_status)
        buffer_full = int(search_answer[1])
        qyentity_pages = int(search_answer[2])
    except TypeError:
        buffer_full = 256
        qyentity_pages = 0
    return buffer_full, qyentity_pages


HOST = 'localhost'                                          # хост принтера
PORT = 8000                                                 # порт, к которому подключен принтер

STATUS_REQUEST = '^0?RS\n\r'
MAILING_STATUS_REQUEST = '^0?SM\n\r'
TEXT_RECORD = '^0=MR{} {}\n\r'
START_PRINT_OUT = '^0!GO\n\r'

ERRORS = {
    '1015': 'Буфер заполнен',
    '1018': 'Неверный или отсутствующий номер индекса',
    '1019': 'Непоследовательный номер индекса',
    '5043': 'Буффер пуст',

}


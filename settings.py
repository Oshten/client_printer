HOST = 'localhost'                                          # хост принтера
PORT = 8000                                                 # порт, к которому подключен принтер

STATUS_REQUEST = '^0?RS'
MAILING_STATUS_REQUEST = '^0?SM'
TEXT_RECORD = '^0=MR{} {}'
START_PRINT_OUT = '^0!GO'

ERRORS = {
    '1015': 'Буфер заполнен',
    '1018': 'Неверный или отсутствующий номер индекса',
    '1019': 'Непоследовательный номер индекса',
    '5043': 'Буффер пуст',

}


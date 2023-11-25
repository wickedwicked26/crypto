import logging

bot_info_log = logging.getLogger('ERRORS LOGS')
bot_info_log.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler('errors_log.log')
handler.setFormatter(formatter)
bot_info_log.addHandler(handler)


def bot_error_logs(info):
	bot_info_log.error(f'ERROR : {info}', exc_info=True)


connection_errors_log = logging.getLogger('CONNECTION ERRORS LOGS')
connection_errors_log.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler('connection_errors_log.log')
handler.setFormatter(formatter)
connection_errors_log.addHandler(handler)


def connection_error_logs(info):
	connection_errors_log.error(f'ERROR : {info}', exc_info=True)

binance_api_error_log = logging.getLogger('BINANCE ERRORS LOGS')
binance_api_error_log.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler('binance_errors_log.log')
handler.setFormatter(formatter)
binance_api_error_log.addHandler(handler)


def binance_error_logs(info):
	binance_api_error_log.error(f'ERROR : {info}', exc_info=True)

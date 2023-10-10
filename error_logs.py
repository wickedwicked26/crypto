import logging

bot_info_log = logging.getLogger('BOT INFO LOGS')
bot_info_log.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler('bot_info_log.log')
handler.setFormatter(formatter)
bot_info_log.addHandler(handler)


def bot_error_logs(info):
    bot_info_log.error(f'ERROR : {info}', exc_info=True)

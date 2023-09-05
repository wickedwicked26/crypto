import telebot
from config import telegram_token

bot = telebot.TeleBot(telegram_token)

chat_ids = [5442883627, '1934151160']


def send_graph(symbol, timestamp, message):
    for i in chat_ids:
        user_id = i
        with open(f'{symbol}_{timestamp}.png', 'rb') as image:
            bot.send_photo(user_id, image, caption=message)


def send_message(message):
    for i in chat_ids:
        user_id = i
        bot.send_message(user_id, message)


def send_error(message):
    bot.send_message('5442883627', message)


def send_connection_res(message):
    bot.send_message("5442883627", message)

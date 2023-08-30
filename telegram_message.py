import telebot
from config import telegram_token

bot = telebot.TeleBot(telegram_token)

chat_ids = ['5442883627', '1934151160']

path = '/home/miguel/PycharmProjects/crypto/'


# @bot.message_handler(commands=['getchatid'])
# def get_chat_id(message):
#     chat_id = message.chat.id
#     bot.reply_to(message, f'Ваш чат айди: {chat_id}')
#
#
# def main():
#     bot.polling(none_stop=True)
#
#
# if __name__ == '__main__':
#     main()


def send_graph(symbol, timestamp, message):
    for i in chat_ids:
        user_id = i
        with open(path + f'{symbol}_{timestamp}.png', 'rb') as image:
            bot.send_photo(user_id, image, caption=message)


def send_message(message):
    for i in chat_ids:
        user_id = i
        bot.send_message(user_id, message)


def send_error(message):
    bot.send_message('5442883627', message)


def send_connection_res(message):
    bot.send_message('5442883627', message)

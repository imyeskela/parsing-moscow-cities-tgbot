import telebot
from telebot import types
from settings import TOKEN
from services import parsing_data, search_city, cities

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, привет!'
                                      f'\nКоманды:\n'
                                      f'/parsing - спарсить данные\n'
                                      f'/getinfo <город> - информация о городе')


@bot.message_handler(commands=['parsing'])
def save_data(message):
    if message.chat.type == 'private':
        parsing_data()
        bot.send_message(message.chat.id, 'Данные успешно сохранены')


@bot.message_handler(commands=['getinfo'])
def get_info(message):
    if message.chat.type == 'private':
        try:
            getinfo = message.text.split(maxsplit=1)[1]
            city = message.text[9:]
            txt = 'Численность населения ' + search_city(city).val()['population'] + '\nСсылка на вики' + search_city(city).val()['link']
            bot.send_message(message.chat.id, txt)
        except:
            bot.send_message(message.chat.id, 'Вы неправильно написали город')


@bot.message_handler(content_types=['text'])
def get_cities(message):
        try:
            bot.send_message(message.chat.id, '\n'.join(cities(message.text)))
        except:
            bot.send_message(message.chat.id, 'Города не найдены(')


bot.polling(none_stop=True)
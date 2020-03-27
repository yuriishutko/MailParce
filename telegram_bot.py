from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters
from config.config import TELEGRAM_TOKEN, API_PRIVAT
from datetime import datetime
import mail_parce
import mysql_database
import requests


keyboard = [['\ud83d\udd51', '/update_database', '\ud83d\udc31'],
            ['/new_users', '/exchange', '/start'],
            ['/new_employees']]

RKM = ReplyKeyboardMarkup(
    keyboard=keyboard,
    resize_keyboard=True,
    one_time_keyboard=True
)


def do_start(update: Update,
             context: CallbackContext):  # update - экземпляр класса Updater (так будут доступны подсказки)
    """Обработчик событий (команды) от телеграма"""
    first_name = update.message.chat.first_name
    context.bot.send_message(chat_id=update.message.chat_id, text='Привет, {} :)'.format(first_name))


def do_stop(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text='Пока')


def do_echo(update: Update, context: CallbackContext):
    """Функция, которая обрабатывает все входящие сообщения """
    text = update.message.text  # Получаем текст того, что нам написали
    context.bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=RKM)


def update_database(update: Update, context: CallbackContext):
    """Функция получает непросмотренные сообщения из ящика и заносит данные в базу данных"""
    count = 0
    arr = mail_parce.get_array_of_data()
    if arr:
        for el in arr:
            count += 1
            print(el, count)
            mysql_database.insert_new_data_to_table(el['date'], el['name'], el['department'], el['role'], el['manager'])
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text='Added ' + str(count) + ' ' + 'new positions')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='There are no new messages')


def get_new_message(update: Update, context: CallbackContext):
    """Function gets data from a database and returns it to text field of telegram bot"""
    data = mysql_database.get_data_from_table()
    for el in data:
        date = datetime.strftime(el[0], '%d-%m-%Y')
        context.bot.send_message(chat_id=update.message.chat_id, text=date + '\n' + '\n'.join(el[1:]))


def get_new_users(update: Update, context: CallbackContext):
    time_now = datetime.now()
    str_time = time_now.strftime('%Y.%m.%d')
    new_employees = mysql_database.get_date_of_new_employees(str_time)
    for el in new_employees:
        date = datetime.strftime(el[0], '%d-%m-%Y')
        context.bot.send_message(chat_id=update.message.chat_id, text=date + '\n' + '\n'.join(el[1:]))


def get_human_ccy_mask(ccy):
    # {"ccy":"USD","base_ccy":"UAH","buy":"24.70000","sale":"25.05000"}
    return "{} / {} : {} / {}".format(ccy["ccy"], ccy["base_ccy"], ccy["buy"], ccy["sale"])


def print_exchange(update: Update, context: CallbackContext):
    response = requests.get(API_PRIVAT)
    list_ccy = response.json()
    human_ccy = '\n'.join(list(map(get_human_ccy_mask, list_ccy)))
    context.bot.send_message(chat_id=update.message.chat_id, text=human_ccy)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text='Я не знаю такой команды)')


def main():
    """Основная функция"""
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)  # Создаем updater как экземпляр класса Updater

    # Добавляем обработчик команд
    start_handler = CommandHandler('start', do_start)
    stop_handler = CommandHandler('stop', do_stop)
    get_new_message_handler = CommandHandler('new_employees', get_new_message)
    update_database_handler = CommandHandler('update_database', update_database)
    exchange_handler = CommandHandler('exchange', print_exchange)
    get_new_users_handler = CommandHandler('new_users', get_new_users)
    unknown_handler = MessageHandler(Filters.command, unknown)
    message_handler = MessageHandler(Filters.text, do_echo)

    # Зарегистрируем обработчик в диспетчере который будет сортировать обновления извлеченные в Updater в соответствии
    # с зарегистрированными обработчиками и доставлять их в функцию обратного вызова callback

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(stop_handler)
    updater.dispatcher.add_handler(get_new_message_handler)
    updater.dispatcher.add_handler(update_database_handler)
    updater.dispatcher.add_handler(exchange_handler)
    updater.dispatcher.add_handler(get_new_users_handler)
    updater.dispatcher.add_handler(unknown_handler)

    # Запускаем скачивание обновлений из телеграма
    updater.start_polling()
    # Указываем Updater, чтоб он не закрывался до тех пор пока не обработаются все updates и чтобы код работал до тех
    # пор пока мы сами не захотим его отключить
    updater.idle()


# Пишем код, чтобы наш бот запускался
if __name__ == '__main__':
    main()

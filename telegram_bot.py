from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters
from config.config import TELEGRAM_TOKEN, API_PRIVAT
from datetime import datetime
import mail_parce
import mysql_database
import requests


def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))


def start(update, context: CallbackContext):

    keyboard = [[InlineKeyboardButton("Update database", callback_data='/update_database'),
                 InlineKeyboardButton("New employees", callback_data='/new_employees')],
                [InlineKeyboardButton("All the data \ud83d\udd51", callback_data='/all_the_data')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


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
    start_handler = CommandHandler('start', start)
    get_new_message_handler = CommandHandler('all_the_data', get_new_message)
    update_database_handler = CommandHandler('update_database', update_database)
    exchange_handler = CommandHandler('exchange', print_exchange)
    get_new_users_handler = CommandHandler('new_employees', get_new_users)
    unknown_handler = MessageHandler(Filters.command, unknown)
    # message_handler = MessageHandler(Filters.text, do_echo)

    # Зарегистрируем обработчик в диспетчере который будет сортировать обновления извлеченные в Updater в соответствии
    # с зарегистрированными обработчиками и доставлять их в функцию обратного вызова callback

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(get_new_message_handler)
    updater.dispatcher.add_handler(update_database_handler)
    updater.dispatcher.add_handler(exchange_handler)
    updater.dispatcher.add_handler(get_new_users_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(unknown_handler)

    # Запускаем скачивание обновлений из телеграма
    updater.start_polling()
    # Указываем Updater, чтоб он не закрывался до тех пор пока не обработаются все updates и чтобы код работал до тех
    # пор пока мы сами не захотим его отключить
    updater.idle()


# Пишем код, чтобы наш бот запускался
if __name__ == '__main__':
    main()

import telebot
from telebot import types
from SDK_TBank import get_info_for_instrument, find_last_price
import logging
import configparser
import time

config = configparser.ConfigParser()
config.read("setting.ini")

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN_TG = config['TOKEN']['TOKEN_TG']
bot = telebot.TeleBot(TOKEN_TG)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Получение последней цены')
    btn2 = types.KeyboardButton('Кнопка 2')
    btn3 = types.KeyboardButton('Кнопка 3')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Привет! Выберите кнопку:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Получение последней цены')
def handle_button1(message):
    msg = bot.send_message(message.chat.id, "Введите тикер:")
    bot.register_next_step_handler(msg, process_parameter)


def process_parameter(message):
    find_fig = get_info_for_instrument(message.text)
    markup = types.InlineKeyboardMarkup(row_width=1)

    if len(find_fig) > 1:
        result = f"По тикеру найдено более 1-й ЦБ, выберите необходимую."
        for fig in find_fig:
            button = types.InlineKeyboardButton(text=fig.get('name'), callback_data=fig.get('uid'))
            markup.add(button)
        bot.send_message(message.chat.id, result, reply_markup=markup)
    elif len(find_fig) == 1:
        uid = find_fig[0].get('uid')
        price = find_last_price(uid).get("price")
        name = find_fig[0].get('name')
        currency = find_fig[0].get('currency')
        lot = find_fig[0].get('lot')
        type_ = find_fig[0].get('type')
        date_and_time = find_last_price(uid).get("date_and_time")
        bot.send_message(message.chat.id, f"Цена 1-й бумаги: '{name}': {float(price):.4f} {currency}\n"
                                          f"Лотность: {lot}, стоимость лота: {(float(price) * int(lot)):.4f}\n"
                                          f"Тип бумаги: {type_}\n"
                                          f"Данные получены за {date_and_time}")
    else:
        bot.send_message(message.chat.id, f"Бумага не найдена, проверьте тикер на корректность ввода.")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    uid = call.data
    find_fig = get_info_for_instrument(uid)
    bot.answer_callback_query(call.id)
    price = find_last_price(uid).get("price")
    name = find_fig[0].get('name')
    currency = find_fig[0].get('currency')
    lot = find_fig[0].get('lot')
    type_ = find_fig[0].get('type')
    date_and_time = find_last_price(uid).get("date_and_time")
    bot.send_message(call.message.chat.id, f"Цена 1-й бумаги: '{name}': {float(price):.4f} {currency}\n"
                                           f"Лотность: {lot}, стоимость лота: {(float(price) * int(lot)):.4f}\n"
                                           f"Тип бумаги: {type_}\n"
                                           f"Данные получены за {date_and_time}")


def notify_admin(error_message):
    admin_chat_id = config['ADMIN']['CHAT_ID']
    max_retries = 5
    delay = 5
    attempt = 0

    while attempt < max_retries:
        try:
            bot.send_message(admin_chat_id, error_message)
            logger.info("Сообщение админу отправлено успешно.")
            break
        except Exception as error:
            attempt += 1
            logger.error(f"Попытка {attempt}: Не удалось отправить сообщение админу: {error}")
            if attempt < max_retries:
                time.sleep(delay)
            else:
                logger.critical("Все попытки отправки сообщения админу исчерпаны.")


if __name__ == '__main__':
    while True:
        try:
            logger.info("Запуск бота...")
            bot.polling(none_stop=True)

        except Exception as e:
            error_message = (
                f"⚠️ Произошла ошибка в главном процессе:\n"
                f"Ошибка: {type(e).__name__}\n"
                f"Описание: {str(e)}"
            )
            logger.error(error_message)
            notify_admin(error_message)
            logger.info("Перезапуск бота через 10 секунд...")
            time.sleep(10)

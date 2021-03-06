comment = """
В этом модуле только хэндлеры отправкой сообщений и работой с данными занимаются методы
"""

import logging

logger = logging.getLogger(__name__)

import logging
from telebot.types import Message, CallbackQuery

from t_bot.bot_db import get_user_from_db
from t_bot import bot_methods
from t_bot.telegram_bot import bot
from t_bot import bot_redis
from t_bot import bot_keyboards

logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start', 'help'])
def start_handler(msg: Message):
    user, _flag = get_user_from_db(msg)
    if _flag:
        logger.info(
            f"User {'@' + user.username if user.username else user.first_name + ' ' + user.last_name} was created")
        bot.send_message(user.tg_id, "Это приветственное сообщение для новых юзеров. Должно отправиться один раз.")
    bot_methods.send_welcome(user)


@bot.message_handler(lambda msg: msg.isdigit())
def get_amount_currency_from_user(msg: Message):
    """
    Ловим цифры, предполагаем, что юзер уже на нужном шаге и отправляет сумму перевода
    :param msg:
    :return:
    """
    bot_methods.get_amount_currency_from(user_id=msg.from_user.id, currency=msg.text)


@bot.callback_query_handler(lambda call: call.data == "start_exchanging")
def start_exchanging_handler(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)

    bot_methods.send_start_exchanging(call.message.from_user.id, False)


@bot.callback_query_handler(lambda call: call.data.startswith('currency'))
def get_currency_from(call: CallbackQuery):
    """
    Ловим валюту списания
    :param call:
    :return:
    """

    bot.delete_message(call.message.chat.id, call.message.message_id)
    if "from" in call.data:
        bot_methods.get_currency_from(call.message.from_user.id, call.data.split(":")[-1])
    elif 'to' in call.data:
        bot_methods.get_currency_to(call.message.from_user.id, call.data.split(":")[-1])


@bot.callback_query_handler(lambda call: call.data.startswith("system"))
def get_user_payment_system(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot_methods.get_payment_system_from_user(call.message.from_user.id, call.data.split(':')[-1])
    pass

@bot.callback_query_handler(lambda call: call.data.startswith("exchange") and
                                         any(('yes' in call.data, 'no'  in call.data)))
def get_answer_about_exchange(call):
    bot.delete_message(call.message.chat.id, call.message.from_user.id)
    if call.data.split(":")[-1] == 'no':
        bot_methods.send_start_exchanging(call.message.from_user.id, False)
    else:
        bot_methods.methods.request_wallet_or_card_number(user_id=call.message.from_user.id)

@bot.message_handler(func=lambda msg: "@" in msg.text and '.' in msg.text)
def get_email_handler(msg: Message):
    bot_methods.methods.get_user_email(user_id=msg.from_user.id, data=msg.text)
    pass


@bot.message_handler(func=lambda msg: True)
def get_wallet_type_number_or_something(msg: Message):
    bot_methods.methods.get_wallet_number(user_id=msg.from_user.id, data=msg.text)


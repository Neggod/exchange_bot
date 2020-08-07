from t_bot.telegram_bot import bot
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

    pass


@bot.callback_query_handler(lambda call: call.data == "start_exchanging")
def start_exchanging_handler(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)

    bot_methods.send_start_exchanging(call.message.from_user.id)


@bot.callback_query_handler(lambda call: len(call.data) == 3 and call.data == call.data.upper())
def get_currency_from(call: CallbackQuery):
    """
    Ловим валюту списания
    :param call:
    :return:
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)
    pass


@bot.callback_query_handler(lambda call: call.data.startswith("system"))
def get_user_payment_system(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    pass

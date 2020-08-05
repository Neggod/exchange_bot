<<<<<<< HEAD
from t_bot.telegram_bot import bot
import logging

logger = logging.getLogger(__name__)
=======
import logging
from telebot.types import Message, CallbackQuery

from t_bot.bot_db import get_user_from_db
from t_bot.bot_methods import send_welcome
from t_bot.telegram_bot import bot

logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start', 'help'])
def start_handler(msg: Message):
    user, _flag = get_user_from_db(msg)
    if _flag:
        logger.info(
            f"User {'@' + user.username if user.username else user.first_name + ' ' + user.last_name} was created")
        bot.send_message(user.tg_id, "Это приветственное сообщение для новых юзеров. Должно отправиться один раз.")
    send_welcome(user)


@bot.message_handler(lambda msg: msg.isdigit())
def get_amount_currency_from_user(msg: Message):
    """
    Ловим цифры, предполагаем, что юзер уже на нужном шаге
    :param msg:
    :return:
    """
    pass


@bot.callback_query_handler(lambda call: call.data)
def get_currency_from_user(call: CallbackQuery):
    """
    Ловим валюту списания
    :param call:
    :return:
    """
    pass
>>>>>>> 421c4ab1af272dacf091a97d390a9ca987fde144

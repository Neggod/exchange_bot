from t_bot.models import TelegramUser
from t_bot.telegram_bot import bot, bot_info
from t_bot import bot_messages
from t_bot import bot_keyboards
from t_bot import bot_redis
from telebot.apihelper import ApiException

import logging

logger = logging.getLogger(__name__)


def send_welcome(user: TelegramUser):
    """
    Здесь мы отправляем приветственное сообщение пользователю
    :param user:
    :return:
    """
    kb = bot_keyboards.generate_start_exchanging()
    try:
        bot.send_message(user.tg_id, bot_messages.WELCOME_MESSAGE.format(name=bot_info.username), reply_markup=kb)
    except ApiException:
        logger.error(f"Cannot send message to user {user}")
    except Exception as err:
        logger.error(err)
    return


def send_error(user_id):
    bot.send_message(user_id, bot_messages.ANY_ERROR_MESSAGE)
    return


def send_start_exchanging(user_id):
    """
    It first message for exchanging
    :param user:
    :return:
    """
    bot_redis.create_new_exchange(user_id)
    kb = bot_keyboards.generate_payment_systems_keyboard()
    if kb:
        bot.send_message(user_id, bot_messages.PAYMENT_METHOD_MESSAGE, reply_markup=kb)
    else:
        send_error(user_id)
    return


def get_currency_from():
    """
    Here ask user currency from
    :return:
    """
    pass


def get_amount_currency_from():
    """
    Here ask
    :return:
    """
    pass


def get_payment_system_and_send_currency(user_id):
    """
    Here ask user system from
    :return:
    """
    pass


def get_currency_to():
    """
    Here asc user currency to
    :return:
    """
    pass


def get_system_to():
    """
    here ask user system to
    :return:
    """
    pass


def send_comission():
    pass


def send_yes_no():
    pass


def approve_last_step(state):
    pass

from t_bot.models import TelegramUser
from t_bot.telegram_bot import bot
import logging

logger = logging.getLogger(__name__)


def send_welcome(user: TelegramUser):
    """
    Здесь мы отправляем приветственное сообщение пользователю
    :param user:
    :return:
    """
    pass


def send_start_exchanging(user: TelegramUser):
    """
    It first message for exchanging
    :param user:
    :return:
    """
    pass


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


def get_system_from():
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

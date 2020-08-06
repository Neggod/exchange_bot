import os
import redis

from django.conf import settings
from t_bot.models import TelegramUser
import logging
from telebot.types import Message

logger = logging.getLogger(__name__)

REDIS_STORAGE = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, )


def get_user_from_redis(msg):
    user = REDIS_STORAGE.get(msg.from_user.id)
    if user:
        logger.info(f"User {user.username} getting from cache")
        return user

    raise ValueError("Haven't user in cache.")


def get_currency_from_redis():
    currency = REDIS_STORAGE.get('currency')
    if currency:
        return currency
    raise ValueError("Havent currency in redis")


def set_values_to_redis(key: str = '', value: str = ''):
    logger.info(f"Try set value: {value} for key: {key}")
    if key and value:
        try:
            REDIS_STORAGE.set(key, value)
        except Exception as err:
            logger.error(err)
            return False

        return True
    else:
        logger.warning(f"Cannot set value: {value} for key: {key}")
        return False
    pass


def create_exchange_value_to_redis(*args, **kwargs):
    """
    Здесь будет храниться процесс формирования транзакции
    :param args:
    :param kwargs:
    :return:
    """
    pass


def get_exchange_from_redis(*args, **kwargs):
    """
    Здесь мы будем дёргать транзакцию из редиса
    :param args:
    :param kwargs:
    :return:
    """
    pass


def save_exchange_to_db(*args, **kwargs):
    """
    Здесь мы возьмём данные из редиса и сохраняем в базу (надо сделать в bot_db метод для этого)

    :param args:
    :param kwargs:
    :return:
    """
    pass


def get_payment_systems_from_redis():
    payment_systems = REDIS_STORAGE.get("systems")
    if payment_systems:
        return payment_systems
    raise ValueError("Haven't payment systems in redis")
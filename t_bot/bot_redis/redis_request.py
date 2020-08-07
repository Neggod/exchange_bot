import os
import redis

from django.conf import settings
from t_bot.models import TelegramUser
from t_bot import bot_db
import logging
from telebot.types import Message
from .redis_templates import *

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
        return currency.decode("UTF-8").split(":")
    raise ValueError("Havent currency in redis")


def set_currency_to_redis(values):
    if isinstance(values, str):
        REDIS_STORAGE.set('currency', values, ex=LONG_LIVE_TTL)
    elif isinstance(values, (list, tuple)):
        _values = ":".join(values)
        REDIS_STORAGE.set('currency', _values, ex=LONG_LIVE_TTL)
    else:
        raise ValueError(f"Unknown currency value {values}")


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


def set_api_exchange_system(user_system: str, api_flag: str):
    REDIS_STORAGE.set(user_system, api_flag, ex=LONG_LIVE_TTL)


def get_api_exchange_system(user_system: str):
    return REDIS_STORAGE.get(user_system).decode("UTF-8")


def create_exchange_value_to_redis(*args, **kwargs):
    """
    Здесь будет храниться процесс формирования транзакции
    :param args:
    :param kwargs:
    :return:
    """
    pass


def get_exchange_from_redis(user_id, status=0, *args, **kwargs):
    """
    Здесь мы будем дёргать транзакцию из редиса
    :param status:
    :param args:
    :param kwargs:
    :return:
    """

    answer = EXCHANGE_TEMPLATE
    for k in answer:
        answer[k] = None
    key = EXCHANGE_TEMPLATE_KEY.format(user=str(user_id))
    values = REDIS_STORAGE.get(key)
    if values:
        values = values.decode("UTF-8").split(":")
    else:
        values_db = bot_db.db_request.get_exchange_from_db(user_id, status)
        if not values_db:
            answer["user"] = user_id
            return answer
        values = values_db
    for value in values:
        for k, v in value.split("="):
            answer[k] = value
    return answer



def save_exchange_to_db(user_id, *args, **kwargs):
    """
    Здесь мы возьмём данные из редиса и сохраняем в базу (надо сделать в bot_db метод для этого)
    Возвращает бинарный сигнал: 00 - нечего сохранять 01 - успешно 10 - ошибка

    :param args:
    :param kwargs:
    :return:
    """
    answer = EXCHANGE_TEMPLATE
    for k in answer:
        answer[k] = None
    key = EXCHANGE_TEMPLATE_KEY.format(user=str(user_id))
    values = REDIS_STORAGE.get(key)
    if values:
        for value in values.decode("UTF-8").split(":"):
            for k, v in value.split("="):
                answer[k] = value
        try:
            bot_db.save_exchange_from_redis(answer)

        except Exception as err:
            logger.error(err)
            return 0b10
        else:
            logger.info("Success saving exchange")
            return 0b01
    logger.info("Haven't value into redis")
    return 0b00





def get_payment_systems_from_redis():
    payment_systems = REDIS_STORAGE.get("systems")
    if payment_systems:
        return payment_systems.decode('UTF-8').split(":")
    raise ValueError("Haven't payment systems in redis ")





def set_payment_systems_to_redis(value):
    if isinstance(value, str):
        REDIS_STORAGE.set('systems', value, ex=LONG_LIVE_TTL)
    elif isinstance(value, (list, tuple)):
        _value = ":".join(value)
        REDIS_STORAGE.set('systems', _value, ex=LONG_LIVE_TTL)
    else:
        raise ValueError(f"Unknown value: {value}")


def create_new_exchange(user_id: int):
    # exchange = EXCHANGE_TEMPLATE['user_id'] = user_id
    # тут какой-то метод для добавления в сторадже
    return None

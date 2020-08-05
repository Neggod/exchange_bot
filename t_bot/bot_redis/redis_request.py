import os
import redis

from django.conf import settings
from t_bot.models import TelegramUser
import logging
from telebot.types import Message


logger = logging.getLogger(__name__)


REDIS_STORAGE = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,)


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


def set_values_to_redis(key: str='', value: str=''):
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


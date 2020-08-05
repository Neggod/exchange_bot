from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

from t_bot.bot_db import get_currency_from_db, Currency
from t_bot.bot_redis.redis_request import get_currency_from_redis

import logging


logger = logging.getLogger(__name__)


def generate_currency_keyboard():
    markup = InlineKeyboardMarkup()
    try:
        currency = get_currency_from_redis()
    except ValueError:
        currency = get_currency_from_db()
    else:
        if currency and isinstance(currency[0], str):
            for curr in currency:
                name, value = currency.split("=")
                markup.add(
                    InlineKeyboardButton(name, callback_data=f"currency:{value}"))
            return markup
        elif currency and isinstance(currency[0], Currency):
            for curr in currency:
                markup.add(InlineKeyboardButton(currency.currency, callback_data=f"currency:{currency.currency_code}"))
            return markup
        else:
            logger.warning('Havent currencies in redis and db')
            return None






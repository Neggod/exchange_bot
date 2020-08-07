from django.db.models import QuerySet
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from payments.models import Currency, PaymentSystem

from t_bot import bot_db
from t_bot.bot_redis import redis_request

import logging


logger = logging.getLogger(__name__)

def generate_payment_systems_keyboard():
    markup = InlineKeyboardMarkup()
    systems = None
    try:
        systems = redis_request.get_payment_systems_from_redis()
        for r_system in systems:
            name, code = r_system.split("=")
            markup.add(InlineKeyboardButton(name, callback_data=f"system:{code}"))
        logger.info("Get systems from redis")
        return markup

    except ValueError:
        logger.info("Haven't system in redis")
        systems = bot_db.get_all_allowed_for_user_payment_systems()
        for system in systems:
            markup.add(InlineKeyboardButton(system.pay_system, callback_data=f"system:{system.pay_system_flag}"))
        logger.info("Get systems from db")
    if not systems:
        logger.warning("NOT PAYMENT SYSTEMS NEED ADDED IT")
        markup = None

    return markup


def generate_currency_keyboard():
    markup = InlineKeyboardMarkup()
    try:
        currency = redis_request.get_currency_from_redis()
    except ValueError:
        currency = bot_db.get_all_currencies_from_db()


    if currency and isinstance(currency[0], str):
        for curr in currency:
            name, value = curr.split("=")
            markup.add(
                InlineKeyboardButton(name, callback_data=f"currency:{value}"))
        return markup
    elif currency and isinstance(currency, QuerySet):
        for curr in currency:
            curr: Currency
            markup.add(InlineKeyboardButton(curr.currency, callback_data=f"currency:{curr.currency_code}"))
        return markup

    else:
        logger.warning('Havent currencies in redis and db')
        return None


def generate_start_exchanging():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Сделать обмен", callback_data="start_exchange"))
    return markup
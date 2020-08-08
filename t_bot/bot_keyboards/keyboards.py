from django.db.models import QuerySet
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, ReplyKeyboardRemove
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


def generate_currency_keyboard(allowed=True):
    markup = InlineKeyboardMarkup()
    try:
        currency = redis_request.get_currency_from_redis(allowed)
    except ValueError:
        currency = redis_request.get_currency_from_redis_with_db(allowed)
    if currency:
        prefix = "currency_from"
        if not allowed:
            prefix = "currency_to"

        for curr in currency:
            name, value = curr.split("=")
            markup.add(
                InlineKeyboardButton(name, callback_data=f"{prefix}:{value}"))
        return markup
    return None


def generate_start_exchanging():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Сделать обмен", callback_data="start_exchange"))
    return markup


def remove_keyboards(inline=True):
    if inline:
        return None
    return ReplyKeyboardRemove()


def generate_approve_buttons(create_exchange: bool):
    markup = InlineKeyboardMarkup()
    if create_exchange:
        markup.add(InlineKeyboardButton("Да", callback_data="exchange:yes"))
        markup.add(InlineKeyboardButton("Нет", callback_data="exchange:no"))

    return markup
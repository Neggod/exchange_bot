import redis
from telebot import TeleBot, types
from telebot.types import Message, CallbackQuery, User
from .models import TelegramUser
from payments.models import *
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

bot = TeleBot(settings.TELEGRAM_TOKEN)


# bot.set_webhook("https://neggod.site:443/tg/1269306538:AAE2JTn6nF61E_d3AZk7bHUwLFrKy2W0GPM/",
#                 certificate=(open('', 'r')))


def generate_valute_keyboard():
    markup = types.InlineKeyboardMarkup()
    for currency in Currency.objects.all():
        markup.add(types.InlineKeyboardButton(currency.currency, callback_data=f"currency:{currency.currency_code}"))
    return markup


def start_hello(user: TelegramUser):
    kb = generate_valute_keyboard()
    bot.send_message(user.tg_id, "Выбери валюту перевода", reply_markup=kb)


def get_user_from_redis(msg):
    user = cache.get(msg.from_user.id)
    if user:
        logger.info(f"User {user.username} getting from cache")
        return user

    raise ValueError("Haven't user in cache.")


def get_user_from_redis_or_db(msg: types.Message):
    try:
        user = get_user_from_redis(msg)
    except ValueError as err:
        logger.info(f"{err.args[0]}")
        user, _flag = TelegramUser.objects.get_or_create(tg_id=msg.from_user.id,
                                                         first_name=msg.from_user.first_name,
                                                         username=msg.from_user.username,
                                                         last_name=msg.from_user.last_name)
        return user, _flag
    else:
        return user, True


@bot.message_handler(commands=['start', 'help'])
def start_handler(msg: Message):
    user, _flag = get_user_from_redis_or_db(msg)
    if _flag:
        logger.info(
            f"User {'@' + user.username if user.username else user.first_name + ' ' + user.last_name} was created")
        bot.send_message(user.tg_id, "Это приветственное сообщение для новых юзеров. Должно отправиться один раз.")
    start_hello(user)


def generate_second_keyboard():
    markup = types.InlineKeyboardMarkup()
    for system in PaymentSystem.objects.all():
        markup.add(types.InlineKeyboardButton(system.pay_system, callback_data=f"system:{system.pay_system_flag}"))
    return markup


def send_systems(user):
    kb = generate_second_keyboard()
    bot.send_message(user.tg_id, "Выберите платёжную систему.", reply_markup=kb)

    pass


def set_velue_to_cache(user, param, currency):
    pass


def send_warning(user: TelegramUser, step: str, value: str):
    bot.send_message(user.tg_id, f"Вы прислали некорректные данные {value}")
    start_hello(user)



@bot.callback_query_handler(func=lambda call: call.data.startswith("currency"))
def callback_valute_handle(call: CallbackQuery):
    # logger.info(f"User {'@' + user.username if user.username else user.first_name + ' ' + user.last_name} check currency")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = call.message
    user, _flag = get_user_from_redis_or_db(msg)
    currency: str = call.data.split(':')[-1]
    if len(currency) == 3 and currency.isalpha() and currency == currency.upper():
        logger.info(f"User {'@' + user.username if user.username else user.first_name + ' ' + user.last_name} "
                    f"check currency {currency}")
        set_velue_to_cache(user, 'currency', currency)
        send_systems(user)
    else:
        logger.warning(f"User {user.username} send {currency}")
        send_warning(user, step='currency', value=currency)
        

    # send_systems(user)


@bot.callback_query_handler(func=lambda call: call.data.startswith("system"))
def callback_system_handle(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    link = settings.MY_DOMAIN + "payment/" + call.data.split(":")[-1] + "/"
    kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Оформить перевод", url=link))
    #                                                               url=settings.MY_DOMAIN + "payment/" + call.data.split(":")[-1]+'/'))
    bot.send_message(call.message.chat.id, "Оформить перевод по ссылке.", reply_markup=kb)

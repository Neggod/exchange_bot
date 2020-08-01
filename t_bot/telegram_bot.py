from telebot import TeleBot, types
from telebot.types import Message, CallbackQuery, User
from .models import TelegramUser
from payments.models import *
from django.conf import settings

bot = TeleBot(settings.TELEGRAM_TOKEN)
bot.set_webhook("https://neggod.site:443/tg/1269306538:AAE2JTn6nF61E_d3AZk7bHUwLFrKy2W0GPM/",
                certificate=(open('', 'r')))


def generate_first_keyboard():
    markup = types.InlineKeyboardMarkup()
    for currency in Currency.objects.all():
        markup.add(types.InlineKeyboardButton(currency.currency, callback_data=f"valute:{currency.currency_code}"))
    return markup


def start_hello(user: TelegramUser):
    kb = generate_first_keyboard()
    bot.send_message(user.tg_id, "Выбери валюту", reply_markup=kb)


@bot.message_handler(commands=['start', 'help'])
def start_handler(msg: Message):
    user, _flag = TelegramUser.objects.get_or_create(tg_id=msg.from_user.id,
                                                     first_name=msg.from_user.first_name,
                                                     username=msg.from_user.username,
                                                     last_name=msg.from_user.last_name)
    if _flag:
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


@bot.callback_query_handler(func=lambda call: call.data.startswith("valute"))
def callback_valute_handle(call: CallbackQuery):
    bot.delete_message(call.message.message_id)
    msg = call.message
    user, _flag = TelegramUser.objects.get_or_create(tg_id=msg.from_user.id,
                                                     first_name=msg.from_user.first_name,
                                                     username=msg.from_user.username,
                                                     last_name=msg.from_user.last_name)
    send_systems(user)


@bot.callback_query_handler(func=lambda call: call.data.startswith("system"))
def callback_system_handle(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    link = settings.MY_DOMAIN + "payment/" + call.data.split(":")[-1] + "/"
    kb = types.InlineKeyboardMarkup(types.InlineKeyboardButton("Оформить перевод", url=link))
#                                                               url=settings.MY_DOMAIN + "payment/" + call.data.split(":")[-1]+'/'))
    bot.send_message(call.message.chat.id, "Оформить перевод по ссылке.", reply_markup=kb)


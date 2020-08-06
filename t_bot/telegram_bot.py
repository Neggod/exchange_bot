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
bot_info = bot.get_me()


# bot.set_webhook("https://neggod.site:443/tg/1269306538:AAE2JTn6nF61E_d3AZk7bHUwLFrKy2W0GPM/",
#                 certificate=(open('', 'r')))



from telebot.types import Message, CallbackQuery

from payments.models import Currency, PaymentSystem
from t_bot.models import TelegramUser
import logging

logger = logging.getLogger(__name__)


# TODO add loggers
def get_user_from_db(msg: Message):
    try:
        user = TelegramUser.objects.get(tg_id=msg.from_user.id)
    except TelegramUser.DoesNotExist:
        user = TelegramUser(
            tg_id=msg.from_user.id,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name,
            username=msg.from_user.username
        )
        return user, False
    else:
        return user, True


def get_all_currencies_from_db():
    return Currency.objects.all()


def get_all_allowed_for_user_payment_systems():
    return PaymentSystem.objects.filter(is_user_payment_system=True)

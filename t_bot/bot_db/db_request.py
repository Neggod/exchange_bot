from telebot.types import Message, CallbackQuery

from payments.models import Currency, PaymentSystem, Status, Exchange
from t_bot.models import TelegramUser
from t_bot.bot_redis import EXCHANGE_TEMPLATE, EXCHANGE_TEMPLATE_VALUE
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

# EXCHANGE_TEMPLATE = {
#     "user": None,
#     "amount": None,
#     "currency": None,
#     'system': None,
#     "status": 0
# }
# EXCHANGE_TEMPLATE_VALUE = "currency={currency}:amount={amount}:user_system={user_system}:status={status}"

def get_exchange_from_db(user_id, status=0):
    try:
        user = TelegramUser.objects.get(tg_id=user_id)
    except TelegramUser.DoesNotExist:
        logger.warning(f"User {user_id} does not exist")
        return None
    try:
        status = Status.objects.get(value=status)
        exchange = Exchange.objects.filter(owner=user, status=status).order_by('-updated')[0]
    except Exchange.DoesNotExist:
        logger.warning(f"Haven't exchange for user {user_id} with status={status}")
        return None
    except Exception as err:
        logger.error(err)
        return None
    else:
        string = EXCHANGE_TEMPLATE_VALUE.format(currency=exchange.currency_from.currency_code, amount=exchange.amount,
                                                user_system=exchange.api.payment_system, status=exchange.status.value)
        return string.split(":")



def save_exchange_from_redis(answer):
    return None
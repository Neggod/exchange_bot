from t_bot.models import TelegramUser
from t_bot.telegram_bot import bot, bot_info
from t_bot import bot_messages
from t_bot import bot_keyboards
from t_bot import bot_redis, bot_db
from telebot.apihelper import ApiException

import logging

logger = logging.getLogger(__name__)


def send_welcome(user: TelegramUser):
    """
    Здесь мы отправляем приветственное сообщение пользователю
    :param user:
    :return:
    """
    kb = bot_keyboards.generate_start_exchanging()
    try:
        bot.send_message(user.tg_id, bot_messages.WELCOME_MESSAGE.format(name=bot_info.username), reply_markup=kb)
    except ApiException:
        logger.error(f"Cannot send message to user {user}")
    except Exception as err:
        logger.error(err)
    return


def send_error(user_id):
    bot.send_message(user_id, bot_messages.ANY_ERROR_MESSAGE)
    return


def send_start_exchanging(user_id, empty_redis_exchange=True):
    """
    It first message for exchanging
    :param user_id: 
    :param user:
    :return:
    """
    if empty_redis_exchange:
        bot.send_message(user_id, "Время платёжной сессии истекло. Начните заново")
    bot_redis.create_or_update_new_exchange(user_id)
    kb = bot_keyboards.generate_payment_systems_keyboard()
    if kb:
        bot.send_message(user_id, bot_messages.PAYMENT_METHOD_MESSAGE, reply_markup=kb)
    else:
        send_error(user_id)
    return


def get_currency_from(user_id, currency):
    """
    Here ask user currency from
    :return:
    """
    exchange = bot_redis.create_or_update_new_exchange(user_id, currency_from=currency)
    if exchange["system"]:
        kb = bot_keyboards.generate_currency_keyboard(False)
        if kb:
            bot.send_message(user_id, bot_messages.CURRENCY_TO_MESSAGE, reply_markup=kb)
        else:
            send_error(user_id)
    else:
        send_start_exchanging(user_id)


def generate_exchange_text(exchange):
    text = 'Обмен {amount} {currency_from} на {currency_to}\n\nК оплате: {amount_finish} {currency_from}'



    return text


def get_amount_currency_from(user_id, currency):
    """
    Here ask
    :return:

    """
    exchange = bot_redis.create_or_update_new_exchange(user_id, amount=currency)
    if exchange["system"]:
        kb = bot_keyboards.keyboards.generate_approve_buttons(create_exchange=True)
        text = generate_exchange_text(exchange)
        bot.send_message(user_id, text, reply_markup=kb)
    else:
        send_start_exchanging(user_id)


def get_currency_to(user_id, currency):
    """
    Here asc user currency to
    :return:
    """
    exchange = bot_redis.create_or_update_new_exchange(user_id, currency_to=currency)
    if exchange["system"]:
        min_amount, max_amount = bot_db.get_max_and_min_currency_amount(exchange['system'])
        max_text = ''
        if max_amount != -1:
            max_text += f', максимальная сумма - {max_amount}'
        kb = bot_keyboards.remove_keyboards()

        bot.send_message(user_id, bot_messages.CURRENCY_TO_MESSAGE + max_text + ":", reply_markup=kb)
    else:
        send_start_exchanging(user_id)
    pass


def get_system_to():
    """
    here ask user system to
    :return:
    """
    pass


def send_comission():
    pass


def send_yes_no():
    pass


def approve_last_step(state):
    pass


def get_payment_system_from_user(user_id, payment_system):

    exchange = bot_redis.create_or_update_new_exchange(user=user_id, payment_system=payment_system)
    logger.info(f"Add to redis exchange {exchange} from user {user_id}")
    kb = bot_keyboards.generate_currency_keyboard()
    if kb:
        bot.send_message(user_id, bot_messages.CURRENCY_FROM_MESSAGE, reply_markup=kb)
    else:
        send_error(user_id)

    return None
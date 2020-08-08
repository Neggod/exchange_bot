import string

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


def request_wallet_or_card_number(user_id):
    exchange = bot_redis.get_exchange_from_redis_or_db(user_id=user_id)
    if exchange['system']:
        system = bot_db.get_payment_system(exchange['system'])
        if not system:
            send_error(user_id)
            return
        if not system.wallet_type:
            text = bot_messages.WALLET_MESSAGE
        elif system.wallet_type == 1:
            text = bot_messages.CARD_NUMBER_MESSAGE
        elif system.wallet_type == 2:
            text = bot_messages.NUMBER_MESSAGE
        elif system.wallet_type == 3:
            text = bot_messages.ADRESS_MESSAGE
        bot.send_message(user_id, text)

    else:
        send_start_exchanging(user_id)
    return


def check_wallet_card(data: str):
    dirty_value = data.replace(" ", '').replace("-", '')
    if len(dirty_value) == 16 and dirty_value.isdigit():
        return True
    return False


def check_wallet_telephone(data: str):
    dirty_value = data[1:] if data.startswith('+') else data[:]
    if dirty_value.replace(' ', '').replace('-', '').replace("(", '').replace(")", '').isdigit():
        return True
    return False


def check_wallet_address(data: str):
    if not len(data.strip()) in range(26, 35):
        return False
    for letter in data.strip():
        if letter in string.ascii_letters:
            continue
        elif letter in string.digits:
            continue
        else:
            return False
    else:
        return True


def check_wallet_wallet(data: str):
    if data.strip().isdigit() and len(data) == 14:
        return True
    return False


def generate_exchange_request(exchange: dict):
    pass


def get_wallet_number(user_id, data):
    exchange = bot_redis.get_exchange_from_redis_or_db(user_id)
    if not exchange['system']:
        send_start_exchanging(user_id)
        return
    if not exchange['wallet']:
        if check_wallet_card(data):
            exchange['wallet'] = data

            pass
        elif check_wallet_telephone(data):
            exchange['wallet'] = data

            pass
        elif check_wallet_address(data):
            exchange['wallet'] = data
            pass
        elif check_wallet_wallet(data):
            exchange['wallet'] = data

            pass
        else:
            bot.send_message(user_id, bot_messages.ERROR_MESSAGE)
            return
        bot.send_message(user_id, bot_messages.ADRESS_MESSAGE)
    else:
        if check_wallet_address(data):
            exchange['wallet'] = data
            system = bot_db.get_payment_system(exchange['code'])
            if system.is_needed_email:
                bot.send_message(user_id, bot_messages.EMAIL_MESSAGE)
            else:
                generate_exchange_request(exchange)
        else:
            bot.send_message(user_id, bot_messages.ERROR_MESSAGE)
    return


def check_email(data: str):
    if data.strip().count(" "):
        return False
    good_letters = string.ascii_letters + string.digits + ''.join(['-', '@', '_', '.'])
    for letter in data.strip():
        if letter in good_letters:
            continue
        else:
            return False
    else:
        return True
    pass


def get_user_email(user_id, data: str):
    exchange = bot_redis.get_exchange_from_redis_or_db(user_id)
    if not exchange['system']:
        send_start_exchanging(user_id)

        return None
    if check_email(data):
        exchange['email'] = data
        generate_exchange_request(exchange)
    else:
        bot.send_message(user_id, bot_messages.ERROR_MESSAGE)

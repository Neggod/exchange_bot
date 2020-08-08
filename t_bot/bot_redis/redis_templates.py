# Пока с хэшами не будем заморачиваться
EXCHANGE_TEMPLATE = {
    "user": '',
    "amount": '',
    "currency_from": '',
    "currency_to": '',
    'system': '',
    'wallet': '',
    'wallet_to': '',
    "email": '',
    "status": 0
}
#
# PAYMENT_SYSTEMS_TEMPLATE = {
#     "SYSTEM": "SYSTEM_CODE"
# }
#
# CURRENCIES_TEMPLATE = {
#     "CURRENCY": "CURRENCY_CODE"
# }

EXCHANGE_TEMPLATE_KEY = "exchange:{user}"
EXCHANGE_TEMPLATE_VALUE = "currency_from={currency_from}:currency_to={currency_to}:amount={amount}:" \
                          "user_system={user_system}:status={status}"

SYSTEM_TEMPLATE_KEY = "system:{system}"

CURRENCY_TEMPLATE = "{currency}={currency_code}"

LONG_LIVE_TTL = 60 * 60 * 24  # время жизни постоянных позиций как системы оплаты, валюты
SHORT_LIVE_TTL = 60 * 20  # время жизни коротких позиций

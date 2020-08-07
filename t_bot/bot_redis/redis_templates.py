# Пока с хэшами не будем заморачиваться
EXCHANGE_TEMPLATE = {
    "user": None,
    "amount": None,
    "currency": None,
    'system': None,
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
EXCHANGE_TEMPLATE_VALUE = "currency={currency}:amount={amount}:user_system={user_system}:status={status}"

LONG_LIVE_TTL = 60 * 60 * 24         # время жизни постоянных позиций как системы оплаты, валюты
SHORT_LIVE_TTL = 60 * 20             # время жизни коротких позиций
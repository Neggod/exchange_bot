# Пока с хэшами не будем заморачиваться
# EXCHANGE_TEMPLATE = {
#     "user_id": None,
#     "amount": None,
#     "currency_to": None,
#     'currency_from': None,
#     "status": 0
# }
#
# PAYMENT_SYSTEMS_TEMPLATE = {
#     "SYSTEM": "SYSTEM_CODE"
# }
#
# CURRENCIES_TEMPLATE = {
#     "CURRENCY": "CURRENCY_CODE"
# }

LONG_LIVE_TTL = 60 * 60 * 24         # время жизни постоянных позиций как системы оплаты, валюты
SHORT_LIVE_TTL = 60 * 20             # время жизни коротких позиций
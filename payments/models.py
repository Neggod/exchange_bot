from decimal import Decimal

from django.db import models
from .choices import *

from t_bot.models import *
"""
user -> payment
payment: from - to - amount - date_create - date_update - status
from == to: payment_system_name - payment_system_short_code
valute: str - str_code

comission

"""

class PaymentSystem(models.Model):
    pay_system = models.CharField(verbose_name="Название платёжной системы", max_length=75)
    pay_system_flag = models.CharField(verbose_name='Короткое название системы на английском языке. 10 знаков',
                                       max_length=10, default='')

    def __str__(self):
        return f"Платёжная система: {self.pay_system}"

    class Meta:
        verbose_name = 'Платёжная система'
        verbose_name_plural = 'Платёжные системы'


# Create your models here.
class PaymentSystemSettings(models.Model):
    payment_system = models.ForeignKey(PaymentSystem, verbose_name="Платёжная система",
                                       on_delete=models.DO_NOTHING, related_name='payment_system')
    wallet = models.CharField(default='', verbose_name="Номер Кошелька", max_length=255)
    public_key = models.CharField(verbose_name="Публичный ключ", blank=True, max_length=255)
    private_key = models.CharField(verbose_name="Приватный ключ", blank=True, max_length=255)

    def __str__(self):
        return f'Настройки платёжной системы {self.payment_system.pay_system}'

    class Meta:
        verbose_name = f'Настройки какой-то системы.'
        verbose_name_plural = 'Настройки платёжных систем'


class Currency(models.Model):
    currency = models.CharField(verbose_name="Название валюты", max_length=75)
    currency_code = models.CharField(verbose_name='Трёхбуквенный код валюты',
                                     help_text='RMB, USD, EUR, RUB etc', max_length=5)

    def __str__(self):
        return f"Валюта {self.currency}"

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class Status(models.Model):

    STATUSES = [
        (0, "Новый платёж"),
        (1, "В обработке"),
        (2, "Оплачено"),
        (3, "Отменено")
    ]

    value = models.IntegerField(verbose_name="Статус платежа", choices=STATUSES, unique=True, default=0)


    def __str__(self):
        return f"Статус: {self.STATUSES[self.value]}"

    class Meta:
        verbose_name = "Статус платежа"
        verbose_name_plural = "Статусы платежей"


class Exchange(models.Model):
    owner = models.ForeignKey(TelegramUser, verbose_name="", on_delete=models.DO_NOTHING, related_name="telegram_user")
    payment_system_from = models.ForeignKey(PaymentSystem, related_name="payment_system_from",
                                            on_delete=models.DO_NOTHING, verbose_name="Откуда переводим")
    payment_system_to = models.ForeignKey(PaymentSystem, on_delete=models.DO_NOTHING,
                                          related_name="payment_system_to",
                                          verbose_name="Куда переводим")
    currency_from = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, verbose_name="Валюта отправления",
                                      related_name="currency_from")
    currency_to = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, verbose_name='Валюта получения',
                                    related_name='currency_to')
    amount = models.DecimalField(verbose_name="Сумма отправления",
                                 default=Decimal(1.0),
                                 max_digits=10,
                                 decimal_places=2)
    created = models.DateTimeField(verbose_name="Дата создания платежа", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего изменения", auto_now=True)
    status =  models.ForeignKey(Status, verbose_name="Статус платежа", on_delete=models.PROTECT)
    # course = models.DecimalField(verbose_name="Курс обмена",
    #                              help_text='валюта отправления * на курс обмена = валюта получения',
    #                              default=Decimal(1.0),
    #                              max_digits=10,
    #                              decimal_places=2)
    # comission = models.IntegerField(verbose_name='Комиссия', help_text='Указать проценты, а не долю от целого '
    #                                                                    '(если 5.5% - указать 5.5, а не 0.055)',
    #                                 default=0)

    def __str__(self):
        return f'Перевод пользователя {self.owner} из ' \
               f'{self.payment_system_from.payment_system} в {self.payment_system_to.payment_system}'

    class Meta:
        verbose_name = 'Перевод между системами'
        verbose_name_plural = "Переводы между системами"


class Comission(models.Model):

    value = models.DecimalField(verbose_name="Значение комиссии в %", help_text="5.23 == 5.53%",
                                max_digits=5, decimal_places=2)
    _from = models.ForeignKey(PaymentSystem, verbose_name="Платёжная система, ОТКУДА совершается перевод",
                              on_delete=models.CASCADE, related_name="+")
    _to = models.ForeignKey(PaymentSystem, verbose_name="Платёжная система, КУДА совершается перевод",
                            on_delete=models.CASCADE, related_name="+")
    currency_from = models.ForeignKey(Currency, verbose_name="Валюта А, которую переводим",
                                      on_delete=models.CASCADE, related_name="+")
    currency_to = models.ForeignKey(Currency, verbose_name="Валюта Б, которую получаем",
                                    on_delete=models.CASCADE, related_name="+")
    min_currency_amount = models.IntegerField(verbose_name="Минимальное значение валюты А", default=100)
    max_currency_amount = models.IntegerField(verbose_name="Максимальное значение валюты А", default=-1,
                                              help_text="Указать, если  есть предел у API сиситемя, ОТКУДА "
                                                        "совершается перевод")

    def __str__(self):
        return f"Комиссия и минимальная сумма для перевода {self.currency_from} из {self._from} в {self._to}"

    class Meta:
        verbose_name = 'Комиссия и минимальная сумма'
        verbose_name_plural = "Комиссии и минимальные суммы"
        default_manager_name = "objects"


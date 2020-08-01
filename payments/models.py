from decimal import Decimal

from django.db import models
from .choices import *

from t_bot.models import *


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


class PromoCode(models.Model):
    code = models.CharField(primary_key=True, verbose_name="Промо-код", blank=False, max_length=10)
    status = models.IntegerField(verbose_name="Статус промокода", default=0, choices=promocode_status)
    percent = models.IntegerField(verbose_name='Процент скидки', blank=False)


class Price(models.Model):
    amount = models.FloatField(verbose_name="Сумма к оплате")
    action = models.IntegerField(verbose_name='Тип объявления', default=1,
                                 choices=MAIN_ACTIONS, null=False, blank=False,
                                 help_text='Реклама или продажа')

    def __str__(self):
        return f"Оплата {self.amount} рублей за {MAIN_ACTIONS[self.action][1]}"

    class Meta:
        verbose_name = 'Прайс'
        verbose_name_plural = 'Прайсы'


class Currency(models.Model):
    currency = models.CharField(verbose_name="Название валюты", max_length=75)
    currency_code = models.CharField(verbose_name='Трёхбуквенный код валюты',
                                     help_text='RMB, USD, EUR, RUB etc', max_length=5)

    def __str__(self):
        return f"Валюта {self.currency}"

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class Exchange(models.Model):
    payment_system_from = models.ForeignKey(PaymentSystemSettings, related_name="payment_system_from",
                                            on_delete=models.DO_NOTHING, verbose_name="Откуда переводим")
    payment_system_to = models.ForeignKey(PaymentSystemSettings, on_delete=models.DO_NOTHING,
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
    course = models.DecimalField(verbose_name="Курс обмена",
                                 help_text='валюта отправления * на курс обмена = валюта получения',
                                 default=Decimal(1.0),
                                 max_digits=10,
                                 decimal_places=2)
    comission = models.IntegerField(verbose_name='Комиссия', help_text='Указать проценты, а не долю от целого '
                                                                       '(если 5.5% - указать 5.5, а не 0.055)',
                                    default=0)

    def __str__(self):
        return f'Перевод из {self.payment_system_from.payment_system} в {self.payment_system_to.payment_system}'

    class Meta:
        verbose_name = 'Перевод между системами'
        verbose_name_plural = "Переводы между системами"


class Payment(models.Model):
    type = models.ForeignKey(PaymentSystemSettings, verbose_name="Тип платёжной системы", on_delete=models.DO_NOTHING,
                             related_name='payment_type')
    amount = models.FloatField(verbose_name="Сумма к оплате")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name="Дата оплаты", auto_now=True)
    status = models.IntegerField(verbose_name="Статус платежа", choices=payment_status, default=0)
    special_code = models.BigIntegerField(verbose_name="Спецкод, генерируемый системой", blank=True, null=True)

    def __str__(self):
        return f"Платеж {payment_status[self.status][1]}  на сумму {self.amount} рублей"

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

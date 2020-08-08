from decimal import Decimal

from django.db import models
from .choices import *

from t_bot.models import TelegramUser

"""
user -> payment
payment: from - to - amount - date_create - date_update - status
from == to: payment_system_name - payment_system_short_code
valute: str - str_code

comission

"""


class PaymentSystem(models.Model):
    pay_system = models.CharField(verbose_name="Название платёжной системы", help_text="QIWI, YANDEX, etc",
                                  max_length=50)
    pay_system_flag = models.CharField(verbose_name='Короткое название системы на английском языке.',
                                       help_text=' Не больше 10 знаков',
                                       max_length=10)

    is_user_payment_system = models.BooleanField(verbose_name="Доступна ли система как пользовательская", default=False)

    def __str__(self):
        return f"Платёжная система: {self.pay_system}"

    class Meta:
        verbose_name = 'Платёжная система'
        verbose_name_plural = 'Платёжные системы'


class UserWallet(models.Model):
    owner = models.ForeignKey(TelegramUser, on_delete=models.DO_NOTHING, verbose_name="Пользователь")
    payment_system = models.ForeignKey(PaymentSystem, on_delete=models.DO_NOTHING, related_name="+",
                                       verbose_name="Пользовательская платeжная система")
    wallet = models.CharField(verbose_name="Номер кошелька или карты", max_length=30, blank=True, null=True)

    def __str__(self):
        return f"Кошелёк пользователя {self.owner} в {self.payment_system}"

    class Meta:
        verbose_name_plural = 'Кошельки пользователей'
        verbose_name = "Кошелёк пользователя"


class Currency(models.Model):
    currency = models.CharField(verbose_name="Название валюты", max_length=75)
    currency_code = models.CharField(verbose_name='Трёхбуквенный код валюты',
                                     help_text='RMB, USD, EUR, RUB etc', max_length=5)
    is_user_currency = models.BooleanField(verbose_name="Доступна ли валюта для перевода пользователем", default=False)

    def __str__(self):
        return f"Валюта {self.currency}"

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class Rate(models.Model):
    """
    Тут будет курс обмена рубля к крипте
    """
    currency_from = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="+",
                                      verbose_name="Валюта списания")
    currency_to = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="+",
                                    verbose_name="Валюта получения")
    rate = models.DecimalField(verbose_name="Курс обмена",
                               help_text='валюта отправления * на курс обмена = валюта получения', max_digits=10,
                               decimal_places=6)


    def __str__(self):
        return f"Курс обмена {self.currency_from} на {self.currency_to}"

    class Meta:
        verbose_name = "Курс обмена"
        verbose_name_plural = "Курсы обмена"


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

    def __str__(self):
        return f"Комиссия и минимальная сумма для перевода {self.currency_from} из {self._from} в {self._to}"

    class Meta:
        verbose_name = 'Комиссия и минимальная сумма'
        verbose_name_plural = "Комиссии и минимальные суммы"
        default_manager_name = "objects"


class PaymentSystemAPI(models.Model):
    """
    Модель платёных апи (пока 3 штуки)
    Cюда добавим
    """
    _API = (
        (0, 'Обменка'),
        (1, 'adgroup'),
        (2, 'westallet')
    )
    id = models.IntegerField(verbose_name="Тип апи", choices=_API, default=0, unique=True)
    payment_system = models.ForeignKey(PaymentSystem, verbose_name="Платёжная система",
                                 help_text="Приоритет для данной системы", on_delete=models.CASCADE)
    rate = models.ForeignKey(Rate, verbose_name="Курс обмена", on_delete=models.DO_NOTHING)
    comission = models.ForeignKey(Comission, on_delete=models.DO_NOTHING, default=50, verbose_name="Комиссия за перевод")
    min_currency_amount = models.IntegerField(verbose_name="Минимальное значение валюты А", default=100)
    max_currency_amount = models.IntegerField(verbose_name="Максимальное значение валюты А", default=-1,
                                              help_text="Указать, если  есть предел у API системы, ОТКУДА "
                                                        "совершается перевод")

    def __str__(self):
        return f"Настройки для АПИ Платёжной системы {self.name}"

    class Meta:
        verbose_name = 'Настройки для АПИ Платёжной системы'
        verbose_name_plural = "Настройки для АПИ Платёжных систем"


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
    api = models.ForeignKey(PaymentSystemAPI, related_name="payment_system_from",
                                            on_delete=models.DO_NOTHING,
                            verbose_name="Какой АПИ используется")

    currency_from = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, verbose_name="Валюта отправления",
                                      related_name="currency_from")
    currency_to = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, verbose_name='Валюта получения',
                                    related_name='currency_to')
    amount = models.DecimalField(verbose_name="Сумма отправления",
                                 default=Decimal(1.0),
                                 max_digits=10,
                                 decimal_places=5)
    created = models.DateTimeField(verbose_name="Дата создания платежа", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего изменения", auto_now=True)
    status = models.ForeignKey(Status, verbose_name="Статус платежа", on_delete=models.PROTECT)

    # course = models.DecimalField(verbose_name="Курс обмена",
    #                              help_text='валюта отправления * на курс обмена = валюта получения',
    #                              default=Decimal(1.0),
    #                              max_digits=10,
    #                              decimal_places=2)
    # comission = models.IntegerField(verbose_name='Комиссия', help_text='Указать проценты, а не долю от целого '
    #                                                                    '(если 5.5% - указать 5.5, а не 0.055)',
    #                                 default=0)

    def __str__(self):
        return f'Перевод пользователя {self.owner} через  ' \
               f'{self.api.name}'

    class Meta:
        verbose_name = 'Перевод между системами'
        verbose_name_plural = "Переводы между системами"


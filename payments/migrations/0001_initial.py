# Generated by Django 3.0.8 on 2020-08-01 12:03

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('t_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=75, verbose_name='Название валюты')),
                ('currency_code', models.CharField(help_text='RMB, USD, EUR, RUB etc', max_length=5, verbose_name='Трёхбуквенный код валюты')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
            },
        ),
        migrations.CreateModel(
            name='PaymentSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_system', models.CharField(max_length=75, verbose_name='Название платёжной системы')),
                ('pay_system_flag', models.CharField(default='', max_length=10, verbose_name='Короткое название системы на английском языке. 10 знаков')),
            ],
            options={
                'verbose_name': 'Платёжная система',
                'verbose_name_plural': 'Платёжные системы',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(0, 'Новый платёж'), (1, 'В обработке'), (2, 'Оплачено'), (3, 'Отменено')], default=0, unique=True, verbose_name='Статус платежа')),
            ],
            options={
                'verbose_name': 'Статус платежа',
                'verbose_name_plural': 'Статусы платежей',
            },
        ),
        migrations.CreateModel(
            name='PaymentSystemSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet', models.CharField(default='', max_length=255, verbose_name='Номер Кошелька')),
                ('public_key', models.CharField(blank=True, max_length=255, verbose_name='Публичный ключ')),
                ('private_key', models.CharField(blank=True, max_length=255, verbose_name='Приватный ключ')),
                ('payment_system', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment_system', to='payments.PaymentSystem', verbose_name='Платёжная система')),
            ],
            options={
                'verbose_name': 'Настройки какой-то системы.',
                'verbose_name_plural': 'Настройки платёжных систем',
            },
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('1'), max_digits=10, verbose_name='Сумма отправления')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания платежа')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('currency_from', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='currency_from', to='payments.Currency', verbose_name='Валюта отправления')),
                ('currency_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='currency_to', to='payments.Currency', verbose_name='Валюта получения')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='telegram_user', to='t_bot.TelegramUser', verbose_name='')),
                ('payment_system_from', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment_system_from', to='payments.PaymentSystem', verbose_name='Откуда переводим')),
                ('payment_system_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment_system_to', to='payments.PaymentSystem', verbose_name='Куда переводим')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payments.Status', verbose_name='Статус платежа')),
            ],
            options={
                'verbose_name': 'Перевод между системами',
                'verbose_name_plural': 'Переводы между системами',
            },
        ),
        migrations.CreateModel(
            name='Comission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, help_text='5.23 == 5.53%', max_digits=5, verbose_name='Значение комиссии в %')),
                ('min_currency_amount', models.IntegerField(default=100, verbose_name='Минимальное значение валюты А')),
                ('max_currency_amount', models.IntegerField(default=-1, help_text='Указать, если  есть предел у API сиситемя, ОТКУДА совершается перевод', verbose_name='Максимальное значение валюты А')),
                ('_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='payments.PaymentSystem', verbose_name='Платёжная система, ОТКУДА совершается перевод')),
                ('_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='payments.PaymentSystem', verbose_name='Платёжная система, КУДА совершается перевод')),
                ('currency_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='payments.Currency', verbose_name='Валюта А, которую переводим')),
                ('currency_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='payments.Currency', verbose_name='Валюта Б, которую получаем')),
            ],
            options={
                'verbose_name': 'Комиссия и минимальная сумма',
                'verbose_name_plural': 'Комиссии и минимальные суммы',
                'default_manager_name': 'objects',
            },
        ),
    ]
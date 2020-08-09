from django.contrib import admin
from payments.models import *


# Register your models here.
# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('type', 'amount', 'user', 'status', 'date')
#
#     search_fields = ['type', 'amount', 'user', 'status', 'date']


@admin.register(PaymentSystemAPI)
class PaymentSystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_system')

    search_fields = ['name', 'payment_system']


@admin.register(PaymentSystem)
class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ('pay_system',)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency', 'currency_code')


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'payment_system_from', 'payment_system_to', 'currency_from', 'amount')


@admin.register(Comission)
class ComissionAdmin(admin.ModelAdmin):
    list_display = '_from', '_to', 'currency_from', 'currency_to', 'value', 'min_currency_amount'




from django.contrib import admin
from payments.models import *


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'user', 'status', 'date')

    search_fields = ['type', 'amount', 'user', 'status', 'date']


@admin.register(PaymentSystemSettings)
class PaymentSystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('payment_system', 'wallet')

    search_fields = ['payment_system', 'wallet']

@admin.register(PaymentSystem)
class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ('pay_system',)

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency', 'currency_code')


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('payment_system_from', 'payment_system_to', 'currency_from', 'amount')



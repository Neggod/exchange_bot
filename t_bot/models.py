from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class TelegramUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    tg_id = models.BigIntegerField(verbose_name="ID в Telegram", unique=True)
    username = models.CharField(verbose_name='Telegram username', help_text="Без @", max_length=74,
                                blank=True, null=True)
    first_name = models.CharField(verbose_name='Имя в ТГ', max_length=74,
                                  blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия в ТГ', max_length=74,
                                 blank=True, null=True)
    
    def __str__(self):
        return f"Пользователь ТГ: {'@' + self.username if self.username else self.first_name + ' ' + self.last_name}"
    
    class Meta:
        verbose_name = "Пользователь Телеграм"
        verbose_name_plural = "Пользователи Телеграм"

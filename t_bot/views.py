import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from telebot import types

from t_bot.telegram_bot import bot


@csrf_exempt
def tg_webhook(request):
    _json = json.loads(request.body.decode("utf-8"))
    bot.process_new_updates([types.Update.de_json(upd) for upd in _json['result']])
    return HttpResponse('OK')

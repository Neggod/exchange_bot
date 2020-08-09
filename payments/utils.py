import base64
import hashlib
import logging
import string
from random import choice
from .models import Exchange
import payments.adgroup_api as adgroup_api
import payments.westwallet_api as westwallet_api
import payments.obmenka_api as obmenka_api

from django.conf import settings


logger = logging.getLogger(__name__)


def generate_obmenka_sign(form_data: str):

    logger.info("Generating sign for acquairing obmenka ua")
    salt = settings.ACQUIRING_SALT.encode("UTF-8")
    # salt = variables.ACQUIRING_TEST_SALT.encode("UTF-8")
    return base64.b64encode(
        hashlib.md5(
            salt +
            base64.b64encode(hashlib.sha1(
                    form_data.encode("UTF-8")
                ).digest()
            ) +
            salt).digest()
    ).decode()

def generate_secret():
    secret = ''.join([choice(string.ascii_letters + string.digits) for _ in range(40)])
    return secret

def get_api(exchange: Exchange):
    _API = (
        ('obmenka', 'Обменка'),
        ('adgroup', 'adgroup'),
        ('westwallet', 'westallet')
    )
    if exchange.api.name == "obmenka":
        return obmenka_api
    elif exchange.api.name == "adgroup":
        return adgroup_api
    elif exchange.api.name == "westwallet":
        return westwallet_api

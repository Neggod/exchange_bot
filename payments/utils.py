import base64
import hashlib
import logging
import string
from random import choice

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


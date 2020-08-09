from payments.models import Exchange
import requests


def create_request_data_from_exchange(exchange: Exchange) -> dict:
    fields = {}
    return fields
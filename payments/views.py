from collections import OrderedDict
from http.client import HTTPResponse

from django.contrib.auth.decorators import permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect


# Create your views here.
# redirect()# TODO!!!
from payments.models import Exchange


@permission_required('admin.can_add_log_entry')
def qiwi_generate(request: WSGIRequest):
    comment = request.GET.get('qw')[0]


def yandex_money_generate(request):
    print(request)


def webmoney_generate(request):
    print(request)


def test_generate(request: WSGIRequest, system):
    print(system)
    print(request.path)
    return render(request, "payments/hello.html", {'system': system})


def obmenka_payment_generate():
    pass

def westwallet_payment_generate():
    pass

def ad_system_payment_generate():
    pass

PAYMENT_SYSTEMS = {

}
@permission_required('admin.can_add_log_entry')
def validate_form(request: WSGIRequest, secret):
    """
    Обработчик формы введенных в бота данных
    :param request:
    :return:
    """
    # data_dict = OrderedDict()
    # data_dict["CLIENT_ID"] = str(variables.ACQUIRING_CLIENT_NUM)
    # data_dict["INVOICE_ID"] = exchange.uuid
    # data_dict["AMOUNT"] = str(exchange.value)
    # data_dict["CURRENCY"] = "RUR"
    # data_dict["PAYMENT_CURRENCY"] = Cur[exchange.payment_method]["name"]
    # data_dict["SUCCESS_URL"] = f"https://t.me/{bot_name}"
    # data_dict["FAIL_URL"] = f"https://t.me/{bot_name}"
    # data_dict["STATUS_URL"] = f"{variables.SELF_URL}{reverse('validate')}?invoice={exchange_uuid}"
    # data_string = "".join(data_dict.values())
    # data_dict["SIGN_ORDER"] = ";".join(data_dict.keys())
    # data_dict["SIGN"] = generate_sign(data_string)
    exchange = Exchange.objects.get(secret=secret)
    return render(request, "payments/payment.html")


def success_payment(request: WSGIRequest):
    """
    Обработчик успешного платежа
    :param request:
    :return:
    """
    return render(request, 'payments/payment_status/success.html')


def fail_payment(request: WSGIRequest):
    """
    Обработчик неуспешного платежа
    :param request:
    :return:
    """
    return render(request, "payments/payment_status/fail.html")


def status_payment(request: WSGIRequest):
    """
    Обработчик статуса платежа
    :param request:
    :return:
    """

    return render(request, "payments/payment_status/status.html")




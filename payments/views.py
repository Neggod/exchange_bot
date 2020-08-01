from http.client import HTTPResponse

from django.contrib.auth.decorators import permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect


# Create your views here.
# redirect()# TODO!!!

@permission_required('admin.can_add_log_entry')
def qiwi_generate(request: WSGIRequest):
    comment = request.GET.get('qw')[0]
    return redirect(f'https://oplata.qiwi.com/create?publicKey'
                    f'=48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPwoVBExVL34tUKumGQDNiKkb4rn4aeGLkPkKhFQUUGi8f8WtvSJRvJ7ZVxosik4Fx6c6w2dLHK2PzKi4667BiUcEmddjcFVR2QkPvWvfxX&billid=123123123&amount=300&comment={comment}')


def yandex_money_generate(request):
    print(request)


def webmoney_generate(request):
    print(request)

def test_generate(request: WSGIRequest, system):
    print(system)
    print(request.path)
    return render(request, "payments/hello.html", {'system': system})

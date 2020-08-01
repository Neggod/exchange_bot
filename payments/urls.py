from django.urls import path
from django.conf.urls.static import static
from payments.views import *
from . import views

urlpatterns = [
    path('qiwi/', qiwi_generate),
    path('ym/', yandex_money_generate),
    path('wm/', webmoney_generate),
    path('<str:system>/', test_generate)

]

from django.urls import path
from django.conf.urls.static import static
from payments.views import *
from . import views

urlpatterns = [
    path('success/', success_payment),
    path('fail/', fail_payment),
    path('wm/', webmoney_generate),
    path('<str:secret>/', test_generate)

]

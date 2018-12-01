from django.conf.urls import url

from ssop_app import views

urlpatterns = [
    url(r'enter_pin$', views.enter_pin, name='enter_pin'),
    url(r'send_pin', views.send_pin, name='send_pin'),
    url(r'validate', views.validate, name='validate'),
]

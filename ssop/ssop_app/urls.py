from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'user_registration$', views.user_registration, name='user_registration'),
    url(r'register_user$', views.register_user, name='register_user'),
    url(r'company_registration$', views.company_registration, name='company_registration'),
    url(r'register_company$', views.register_company, name='register_company'),
    url(r'send_sms', views.send_sms, name='send_sms'),

]
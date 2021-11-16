from django.conf.urls import url, include
from django.contrib import admin
from polls import views

urlpatterns = [
    url(r'^send/sms/', views.send_sms),
    url(r'^register/', views.register,name='register'), # "app01:register"
]


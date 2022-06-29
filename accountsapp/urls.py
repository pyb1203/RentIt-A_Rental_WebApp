
from django.urls import path
from .views import *

urlpatterns=[
    path('register',sign_up,name='register' ),
    path('verify',verify,name='verify' ),
    path('login', sign_in, name='login' ),
    path('logout',logout,name ='logout')


]

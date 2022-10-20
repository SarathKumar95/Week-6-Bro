from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signup, name='user'),
    path('signin', views.signin, name='signin'),
    path('home', views.home, name='home'),
    path('out', views.out, name='out')
]

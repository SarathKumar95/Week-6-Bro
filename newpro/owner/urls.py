from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signup, name='user'),
    path('signin', views.signin, name='signin'),
    path('home', views.home, name='home'),
    path('out', views.out, name='out'),
    path('owner', views.owner, name='owner'),
    path('create', views.create_user, name='create'),
    # path('update', views.update_user, name='update'),
    path('delete/<int:id>', views.delete_user, name='delete'),
    path('master', views.master, name='master')
]

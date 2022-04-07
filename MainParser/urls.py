from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login, name='main-login'),
    path('', views.index, name='main-index'),
    path('register', views.register, name='main-register'),
    path('logout', views.logout, name='main-logout')
]

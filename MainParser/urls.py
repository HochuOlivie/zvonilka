from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('login', views.login, name='main-login'),
    path('', views.index, name='main-index'),
    path('register', views.register, name='main-register'),
    path('logout', views.logout, name='main-logout'),
    path('ajax/get_table/', views.get_table, name='get_table')
]

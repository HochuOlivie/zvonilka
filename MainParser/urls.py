from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('login', views.login, name='main-login'),
    path('', views.index, name='main-index'),
    path('register', views.register, name='main-register'),
    path('logout', views.logout, name='main-logout'),
    path('ajax/get_table/', views.get_table, name='ajax-get_table'),
    path('ajax/no_call/', views.no_call, name='ajax-no_call'),
    path('ajax/closed/', views.closed, name='ajax-closed'),
    path('ajax/target_ad/', views.target_ad, name='ajax-target_ad'),
    path('ajax/working_status/', views.working_status, name='ajax-working_status'),
]

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('/get_auth_code', views.get_auth_code(request)),
    path('path/', views.callback_url())
]
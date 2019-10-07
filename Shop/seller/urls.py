from django.urls import path
from seller import views

patterns = [
    path('register/', views.register),  # 注册
    path('login/', views.register),  # 登录
]

from django.urls import path
from seller import views

patterns = [
    path('register/', views.register)  # 注册
]
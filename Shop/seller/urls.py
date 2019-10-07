from django.urls import path
from seller import views

urlpatterns = [
    path('register/', views.register),  # 注册
    path('login/', views.register),  # 登录
    path('index/', views.register),  # 首页
]

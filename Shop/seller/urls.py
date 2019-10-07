from django.urls import path
from seller import views

urlpatterns = [
    path('register/', views.register),  # 注册
    path('login/', views.login),  # 登录
    path('index/', views.index),  # 首页
    path('logout/', views.logout),  # 首页
]

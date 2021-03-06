from django.urls import path
from seller import views

urlpatterns = [
    path('register/', views.register),  # 注册
    path('login/', views.login),  # 登录
    path('index/', views.index),  # 首页
    path('logout/', views.logout),  # 登出
    path('type_list/', views.type_list),  # 商品类型列表
    path('type_add/', views.type_add),  # 商品类型添加
    path('type_ajax/', views.type_ajax),  # 商品类型验证
    path('goods_list/', views.goods_list),  # 商品类型验证
    path('goods_add/', views.goods_add),  # 商品类型验证
    path('goods_update/', views.goods_update),  # 商品类型验证
    path('goods_delete/', views.goods_delete),  # 商品类型验证
]

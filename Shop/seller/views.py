from django.shortcuts import render, redirect
from seller import forms
from seller import models
import time
import hashlib
import datetime


# 加密函数
def pwd_jm(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()


# Create your views here.
# 卖家注册
def register(request):
    register_form_obj = forms.RegisterForm()
    error_msg = ''
    # post 提交
    if request.method == 'POST':
        register_form_obj = forms.RegisterForm(request.POST, request.FILES)
        if register_form_obj.is_valid():
            # 获取数据
            data = register_form_obj.cleaned_data
            name = data.get('name')
            nick_name = data.get('nick_name')
            password = data.get('password')
            photo = data.get('photo')
            # 判断用户名是否被注册（数据库是否存在此用户名）
            seller_obj = models.Seller.objects.filter(name=name).first()
            # 不存在 保存数据
            # 保存图片
            time_tmp = str(int(time.time()))
            path = 'static/photo/' + time_tmp + photo.name
            with open(path, 'wb') as f:
                for content in photo:
                    f.write(content)
            # 密码加密
            password = pwd_jm(password)
            if not seller_obj:
                # 保存数据库
                models.Seller.objects.create(
                    name=name,
                    nickname=nick_name,
                    password=password,
                    photo='photo/' + time_tmp + photo.name
                )
                # 重定向登录页
                return redirect('/seller/login/')
            error_msg = '用户名已注册，请重新输入'
    # get方式 返回注册页面
    return render(request, 'seller/register.html', {'register_form_obj': register_form_obj, 'error_msg': error_msg})


def login(request):
    login_form_obj = forms.LoginForm()
    error_msg = ''
    if request.method == "POST":
        login_form_obj = forms.LoginForm(request.POST)
        if login_form_obj.is_valid():
            data = login_form_obj.cleaned_data
            name = data.get('name')
            password = data.get('password')
            password = pwd_jm(password)
            seller_obj = models.Seller.objects.filter(name=name, password=password).first()
            if seller_obj:
                # 登录成功
                # 保存session
                request.session['seller_name'] = name
                request.session['seller_id'] = seller_obj.id
                # 重定向到首页
                return redirect('/seller/index/')
            error_msg = '用户名或密码错误'
    return render(request, 'seller/login.html', {'login_form_obj': login_form_obj, 'error_msg': error_msg})


# 首页
def index(request):
    login_time = datetime.datetime.now()
    seller_id = request.session.get('seller_id')
    seller_obj = models.Seller.objects.get(id=seller_id)
    return render(request, 'seller/index.html', {'seller_obj': seller_obj, 'login_time': login_time})

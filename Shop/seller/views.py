from django.shortcuts import render, redirect
from django.http import JsonResponse
from seller import forms
from seller import models
import time
import hashlib
import datetime
from django.core.paginator import Paginator


# 登录权限 未登录用户跳转至登录页 已登录用户进入对应页 (装饰器实现)
def check_login(func):
    def inner(request):
        name = request.session.get('seller_name')
        if name:
            return func(request)
        else:
            return redirect('/seller/login')

    return inner


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
# @check_login
def index(request):
    login_time = datetime.datetime.now()
    seller_id = request.session.get('seller_id')
    seller_obj = models.Seller.objects.get(id=seller_id)
    return render(request, 'seller/index.html', {'seller_obj': seller_obj, 'login_time': login_time})


# 登出
# @check_login
def logout(request):
    # 删除 session
    request.session.flush()
    # 重定向
    return redirect('/seller/login/')


# 商品类型
# 商品类型列表
def type_list(request):
    type_obj_list = models.GoodType.objects.all()
    # 每页 5 条
    each_num = 5
    paginator = Paginator(type_obj_list, each_num)
    num_pages = paginator.num_pages
    page_num = 1
    try:
        page_num = int(request.GET.get('page', 1))
        page_obj = paginator.page(page_num)
    except Exception:
        if page_num > num_pages:
            page_num = num_pages
        else:
            page_num = 1
        page_obj = paginator.page(page_num)
    return render(request, 'seller/type_list.html', locals())


# 商品添加
def type_add(request):
    error_msg = ''
    type_name = ''
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        type_obj = models.GoodType.objects.filter(name=type_name).first()
        if not type_obj:
            models.GoodType.objects.create(name=type_name)
            return redirect('/seller/type_list')
        error_msg = '此类型已存在,请修改商品类型'
    return render(request, 'seller/type_add.html', {'error_msg': error_msg, 'type_name': type_name})


# 商品类型验证ajax
def type_ajax(request):
    dic = {
        'status': 'true'
    }
    type_name = request.GET.get('type_name')
    type_obj = models.GoodType.objects.filter(name=type_name).first()
    if type_obj:
        dic['status'] = 'false'
    return JsonResponse(dic)


# 商品类型修改
def type_update(request):
    if request.method == 'GET':
        type_id = request.GET.get('id')
        type_obj = models.GoodType.objects.get(id=type_id)
        return render(request, 'seller/type_change.html', {'type_name': type_obj.name})
    else:
        type_id = request.POST.get('id')
        type_name = request.POST.get('type_name')
        type_obj = models.GoodType.objects.filter(name=type_name).first()
        if not type_obj:
            type_obj = models.GoodType.objects.get(id=type_id)
            type_obj.name = type_name
            type_obj.save()
            return redirect('/seller/type_list/')
        error_msg = '此类型已存在，请重新输入'
        return render(request, 'seller/type_change.html', {'type_name': type_name, 'error_msg': error_msg})


# 商品类型删除
def type_delete(request):
    type_id = request.GET.get('id')
    type_obj = models.GoodType.objects.get(id=type_id)
    type_obj.delete()
    return redirect('/seller/type_list/')


# 商品

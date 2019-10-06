from django.shortcuts import render
from seller import forms
from seller import models


# Create your views here.
# 卖家注册
def register(request):
    register_form_obj = forms.RegisterForm()
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
            if not seller_obj:
                pass

    # get方式 返回注册页面
    return render(request, 'seller/register.html', {'register_form_obj': register_form_obj})

# form 组件
from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets as wid, ValidationError
from seller import models


class RegisterForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=32,
        min_length=3,
        # validators=[
        #     RegexValidator(r'^(?!_)[a-zA-Z0-9_\u4e00-\u9fa5]{3，32}$', '用户名输入不符合规范')
        # ],
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名至少输入3位',
            'max_length': '用户名至多输入32位'
        },
        widget=wid.TextInput(attrs={'placeholder': "用户名", 'class': "layui-input", 'id': 'name'})
    )
    nick_name = forms.CharField(
        required=True,
        max_length=32,
        min_length=3,
        error_messages={
            'required': '昵称不能为空',
            'max_length': '昵称至多输入32位'
        },
        validators=[
            RegexValidator(r'^(?!_)[a-zA-Z0-9_\u4e00-\u9fa5]{1,32}$', '昵称由数、字母、下划线、汉字组成')
        ],
        widget=wid.TextInput(attrs={'placeholder': "昵称", 'class': "layui-input"})
    )
    password = forms.CharField(
        required=True,
        max_length=32,
        min_length=6,
        widget=wid.PasswordInput(attrs={'placeholder': "密码", 'class': "layui-input"})
    )
    photo = forms.ImageField(
        required=True,
        widget=wid.FileInput(attrs={'class': 'layui-input'})
    )

    def clean(self):
        data = self.cleaned_data
        name = data.get('name')
        if name:
            seller = models.Seller.objects.filter(name=name).first()
            if seller:
                error = ValidationError('用户名已注册')
                self.add_error('name', error)
                raise error
        return self.cleaned_data


class LoginForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=32,
        min_length=3,
        # validators=[
        #     RegexValidator(r'^(?!_)[a-zA-Z0-9_\u4e00-\u9fa5]{3，32}$', '用户名输入不符合规范')
        # ],
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名至少输入3位',
            'max_length': '用户名至多输入32位'
        },
        widget=wid.TextInput(attrs={'placeholder': "用户名", 'class': "layui-input", 'id': 'name'})
    )
    password = forms.CharField(
        required=True,
        max_length=32,
        min_length=6,
        widget=wid.PasswordInput(attrs={'placeholder': "密码", 'class': "layui-input"})
    )


class GoodsForm(forms.Form):
    class Meta:
        model = models.Goods
        fields = ['goods_num', 'goods_name', 'goods_oprice', 'goods_cprice', 'goods_count', 'goods_desc']
        widgets = {
            'goods_num': wid.TextInput(attrs={'class': 'layui-input', 'id': 'L_email', 'autocomplete': 'off'}),
            'goods_name': wid.TextInput(attrs={'class': 'layui-input', 'id': 'L_username', 'autocomplete': 'off'}),
            'goods_oprice': wid.TextInput(attrs={'class': 'layui-input', 'id': 'L_pass', 'autocomplete': 'off'}),
            'goods_cprice': wid.TextInput(attrs={'class': 'layui-input', 'id': 'L_pass', 'autocomplete': 'off'}),
            'goods_count': wid.NumberInput(attrs={'class': 'layui-input', 'id': 'L_pass', 'autocomplete': 'off'}),
            'goods_desc': wid.TextInput(attrs={'class': 'layui-input', 'id': 'L_repass', 'autocomplete': 'off'}),
        }

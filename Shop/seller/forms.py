# form 组件
from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets, ValidationError


class RegisterForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=32,
        min_length=3,
        # validators=[
        #     RegexValidator(r'^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]{3，32}$', '用户名输入不符合规范')
        # ],
        widget=widgets.TextInput(attrs={'placeholder': "用户名", 'class': "layui-input"})
    )
    nick_name = forms.CharField(
        required=True,
        max_length=32,
        min_length=3,
        widget=widgets.TextInput(attrs={'placeholder': "昵称", 'class': "layui-input"})
    )
    password = forms.CharField(
        required=True,
        max_length=32,
        min_length=6,
        widget=widgets.PasswordInput(attrs={'placeholder': "密码", 'class': "layui-input"})
    )
    photo = forms.ImageField(
        required=True,
        widget=widgets.FileInput(attrs={'class':'layui-input'})
    )

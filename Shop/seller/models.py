from django.db import models


# Create your models here.

# 卖家类
class Seller(models.Model):
    name = models.CharField(max_length=32)  # 卖家名称
    nickname = models.CharField(max_length=32)  # 昵称
    password = models.CharField(max_length=64)  # 用户密码
    photo = models.ImageField()  # 头像

    def __str__(self):
        return '<obj name:{}>'.format(self.name)


# 商品类型
class GoodType(models.Model):
    name = models.CharField(max_length=32)  # 类型名称

    def __str__(self):
        return '<obj name:{}>'.format(self.name)

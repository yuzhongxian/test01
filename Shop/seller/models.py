from django.db import models
from ckeditor.fields import RichTextField


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


# 商品
class Goods(models.Model):
    goods_num = models.CharField(max_length=12)  # 商品
    goods_name = models.CharField(max_length=32)  # 商品名称
    goods_oprice = models.DecimalField(max_digits=12, decimal_places=2)  # 商品原价
    goods_cprice = models.DecimalField(max_digits=12, decimal_places=2)  # 商品现价
    goods_count = models.IntegerField()  # 商品库存
    goods_desc = models.CharField(max_length=128)  # 商品描叙
    goods_detail = RichTextField()  # 商品详情
    # 关系 类型 对 商品
    type = models.ForeignKey(to='GoodType', on_delete=models.CASCADE)
    # 卖家
    seller = models.ForeignKey(to='Seller', on_delete=models.CASCADE)

    def __str__(self):
        return '<object name:{}>'.format(self.goods_name)


class GoodsImage(models.Model):
    image_path = models.CharField(max_length=128)  # 图片地址
    # 关系 图像 商品  多对一
    goods = models.ForeignKey(to='Goods', on_delete=models.CASCADE)

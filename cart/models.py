from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from goods.models import Product  # 假设商品模型在 goods app 中

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # 一个用户不能对同一商品添加多个条目

    def __str__(self):
        return f"{self.user.username} 的购物车 - {self.product.name}"


from django.db import models
from django.contrib.auth.models import User

#
# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="用户")
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总价")
#     status = models.CharField(max_length=20, choices=[('待支付', '待支付'), ('已支付', '已支付')], default='待支付',
#                               verbose_name="订单状态")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
#
#     def __str__(self):
#         return f"订单{self.id} - {self.status}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="用户")
    status = models.CharField(
        max_length=20,
        choices=[('待支付', '待支付'), ('已支付', '已支付')],
        default='待支付',
        verbose_name="订单状态"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总价")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f"订单{self.id} - {self.status}"

from store.models import Shop

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="所属订单")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    store = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="商店")  # 从 product.store 赋值
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")  # 冗余保存

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

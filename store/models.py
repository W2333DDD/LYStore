from django.db import models

# Create your models here.


# store/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# store/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# store/models.py

class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="商家用户")
    name = models.CharField(max_length=100, verbose_name="商店名称")
    avatar = models.ImageField(upload_to='shop_avatars/', verbose_name="商店头像")
    description = models.TextField(blank=True, verbose_name="商店简介")

    real_name = models.CharField(max_length=100, verbose_name="注册人姓名")
    email = models.EmailField(verbose_name="邮箱")
    phone = models.CharField(max_length=20, verbose_name="手机号")
    id_front = models.ImageField(upload_to='id_cards/', verbose_name="身份证正面")
    id_back = models.ImageField(upload_to='id_cards/', verbose_name="身份证反面")

    is_approved = models.BooleanField(default=False, verbose_name="是否通过审核")  # ✅ 审核字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    total_gold_coins = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name




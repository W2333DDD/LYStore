from django.contrib.auth.models import AbstractUser
from django.db import models


# 自定义用户模型
class CustomUser(AbstractUser):
    # 可以根据需求添加更多字段
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="电话号码")
    address = models.TextField(blank=True, null=True, help_text="用户地址")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="用户头像")

    def __str__(self):
        return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# 自定义用户模型
class CustomUser(AbstractUser):
    # 可以根据需求添加更多字段
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="电话号码")
    address = models.TextField(blank=True, null=True, help_text="用户地址")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="用户头像")
    gold_coins=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.username

class GoldRecharge(models.Model):
    STATUS_CHOICES = [
        ('waiting', '待审核'),
        ('done', '已到账'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 判断是否由 waiting 改成了 done
        print(f'修改前用户金额是{self.user.gold_coins}')
        if self.pk:
            old = GoldRecharge.objects.get(pk=self.pk)
            if self.status=='done':
                self.user.gold_coins += self.amount
                self.user.save()
                print(f'修改后用户金额是{self.user.gold_coins}')
        print(f"名称是{self.user.username}")
        super().save(*args, **kwargs)
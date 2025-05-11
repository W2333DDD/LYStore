from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from goods.models import Product

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name="商品")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="评论用户")
    text = models.TextField("评论内容", max_length=1000, blank=True)
    image = models.ImageField("评论图片", upload_to='comment_images/', blank=True, null=True)
    video = models.FileField("评论视频", upload_to='comment_videos/', blank=True, null=True)
    created_at = models.DateTimeField("评论时间", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 对 {self.product.name} 的评论"

from django.db import models
from store.models import Shop


class Product(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="所属商店"
    )

    name = models.CharField(max_length=100, verbose_name="商品名称")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品价格")
    description = models.TextField(blank=True, verbose_name="商品简介")
    category = models.TextField(null=False,default='未分类',verbose_name='商品分类')
    image = models.ImageField(upload_to='product_images/', verbose_name="商品图片", blank=True, null=True)
    video = models.FileField(upload_to='product_videos/', verbose_name="商品视频", blank=True, null=True)
    tripo_3d_model = models.FileField(upload_to='3d_models/', verbose_name="3D模型",null=True, blank=True)


    tripo_task_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tripo3D任务ID")
    tripo_status = models.CharField(max_length=50, blank=True, null=True, verbose_name="3D生成状态", default='未开始')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.name} ({self.shop.name})"

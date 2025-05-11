from django.contrib import admin

# Register your models here.
# store/admin.py

from django.contrib import admin
from .models import Shop
from goods.models import Product
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('name', 'owner__username')
    list_editable = ('is_approved',)  # ✅ 支持直接编辑审核状态
    readonly_fields = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'price', 'created_at')

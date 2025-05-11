from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)

from django.contrib import admin
from .models import GoldRecharge

@admin.register(GoldRecharge)
class GoldRechargeAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'created_at']
    list_filter = ['status']
    actions = ['mark_as_done']

    @admin.action(description='标记为已到账')
    def mark_as_done(self, request, queryset):
        for record in queryset:
            if record.status != 'done':
                record.status = 'done'
                record.user.gold_coins += record.amount
                record.user.save()
                record.save()

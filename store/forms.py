# store/forms.py

from django import forms
from .models import Shop

class ShopRegisterForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            'name', 'avatar', 'description',
            'real_name', 'email', 'phone',
            'id_front', 'id_back'
        ]
        labels = {
            'name': "商店名称",
            'avatar': "商店头像",
            'description': "商店简介",
            'real_name': "注册人姓名",
            'email': "邮箱",
            'phone': "手机号",
            'id_front': "身份证正面",
            'id_back': "身份证反面",
        }

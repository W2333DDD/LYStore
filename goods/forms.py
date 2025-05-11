from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    generate_3d_model = forms.BooleanField(
        required=False,
        label="是否生成3D模型"
    )
    tripo_api_key = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '请输入 Tripo3D API Key'}),
        label="Tripo3D API Key"
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'video']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': '商品名称',
            'description': '商品简介',
            'price': '商品价格',
            'image': '商品图片',
            'video': '商品视频',
        }

    def clean(self):
        cleaned_data = super().clean()
        generate_3d_model = cleaned_data.get('generate_3d_model')
        tripo_api_key = cleaned_data.get('tripo_api_key')

        if generate_3d_model and not tripo_api_key:
            self.add_error('tripo_api_key', '若选择生成3D模型，必须提供 API Key。')

        return cleaned_data

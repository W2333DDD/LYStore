from django.shortcuts import render
from store.models import Shop
from goods.models import Product
# Create your views here.


def firstpage_show(request):
    shop1 = Shop.objects.get(name="好好")
    product1=shop1.products.get(name='音箱3d')
    product2=shop1.products.get(name='地球3')
    product3=shop1.products.get(name='网球3')
    product4=shop1.products.get(name='网球2')
    context = {'product1':product1,'product2':product2,'product3':product3,'product4':product4}
    return render(request, 'imitatejd.html',context=context)


def usr_login(request):
    return render(request,'usr_logoin.html')





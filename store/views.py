from django.shortcuts import render

# Create your views here.


# store/views.py

from django.shortcuts import render, redirect
from .forms import ShopRegisterForm
from .models import Shop
from django.contrib.auth.decorators import login_required

@login_required
def register_shop(request):
    if request.method == "POST":
        form = ShopRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            return render(request,'register_success.html')
    else:
        form = ShopRegisterForm()

    return render(request, 'store_enroll.html', {'form': form})


from django.contrib.auth.decorators import login_required
from .models import Shop

@login_required
def my_shop(request):
    try:
        shop = Shop.objects.get(owner=request.user)
    except Shop.DoesNotExist:
        return redirect('store:register_shop')

    return render(request, 'my_store.html', {'shop': shop})


# store/views.py
from django.shortcuts import render, get_object_or_404
from .models import Shop

def store_detail(request, pk):
    store = get_object_or_404(Shop, pk=pk)
    return render(request, 'store_detail.html', {'store': store})
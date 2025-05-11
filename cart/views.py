from django.shortcuts import render

# Create your views here.


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import CartItem
from goods.models import Product

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:view')  # 跳转到购物车页面

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart_view.html', {'cart_items': cart_items,'total_price': total_price})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart:view')


from django.shortcuts import render, redirect
from django.conf import settings
from .models import Order

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order
from usr.models import CustomUser

from django.contrib import messages

# def checkout(request):
#     user = request.user
#     cart_items = CartItem.objects.filter(user=user)
#
#     if not cart_items.exists():
#         messages.error(request, '购物车为空，无法结算。')
#         return redirect('cart:view')  # 或跳转到购物车页面
#
#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#     print("用户金币余额：", user.gold_coins)
#     print("订单总价：", total_price)
#
#     if user.gold_coins >= total_price:
#         # 扣除金币
#         user.gold_coins -= total_price
#         user.save()
#
#         # 创建订单
#         order = Order.objects.create(user=user, total_price=total_price, status='completed')
#
#         # （可选）将购物车清空
#         cart_items.delete()
#
#         return render(request, 'payment_success.html', {'order': order})
#     else:
#         messages.error(request, '您的金币不足以支付此次订单，请充值或选择其他支付方式。')
#         return render(request, 'payment.html', {'total_price': total_price})

from .models import Order, OrderItem  # 根据你 app 的结构调整
from django.core.mail import send_mail  # 示例用途
from django.db.models import F

def checkout(request):
    user = request.user
    #cart_items = CartItem.objects.select_related('product__store').filter(user=user)
    cart_items = CartItem.objects.filter(user=user)
    if not cart_items.exists():
        messages.error(request, '购物车为空，无法结算。')
        return redirect('cart:view')

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    print("用户金币余额：", user.gold_coins)
    print("订单总价：", total_price)

    if user.gold_coins >= total_price:
        # 扣除金币
        user.gold_coins = F('gold_coins') - total_price
        user.save()

        # 创建订单
        order = Order.objects.create(user=user, total_price=total_price, status='已支付')

        # 创建 OrderItem，并通知商家
        store_notified = set()
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                store=item.product.shop,
                quantity=item.quantity,
                price=item.product.price
            )

            # 通知商家（例如发送邮件）
            store = item.product.shop
            if store.id not in store_notified:
                store_notified.add(store.id)
                if store.owner.email:
                    send_mail(
                        subject=f"新订单通知 - 订单{order.id}",
                        message=f"亲爱的商家 {store.name}，您有一笔新订单，请及时处理发货。",
                        from_email="3188753874@qq.com",
                        recipient_list=[store.owner.email],
                        fail_silently=True,
                    )

        # 清空购物车
        cart_items.delete()

        return render(request, 'payment_success.html', {'order': order})
    else:
        messages.error(request, '您的金币不足以支付此次订单，请充值后再尝试。')
        return render(request, 'payment.html', {'total_price': total_price})



def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart:view')

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart:view')
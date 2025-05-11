from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm,CustomUserLoginForm
from django.contrib.auth import logout
from store.models import *
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 保存用户
            login(request, user)  # 自动登录
            return redirect('apppage:firstpage')  # 注册成功后跳转到首页
        print('信息不正确')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usr_enroll.html', {'form': form})

from django.contrib.auth import authenticate

def login_view(request):
    if request.method == 'POST':
        username_or_phone = request.POST.get('username')
        password = request.POST.get('password')

        # 尝试通过用户名找人
        user = authenticate(request, username=username_or_phone, password=password)

        # 如果用户名失败，再尝试用手机号
        if user is None:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                matched_user = User.objects.get(phone=username_or_phone)  # 确保你有 phone 字段
                user = authenticate(request, username=matched_user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            print('登录成功')
            return redirect('apppage:firstpage')
        else:
            print('登录失败，用户名或密码错误')
            form = CustomUserLoginForm()
    else:
        form = CustomUserLoginForm()
    return render(request, 'usr_logoin.html', {'form': form})

def logout_view(request):
    logout(request)  # 清除用户的会话
    return redirect('apppage:firstpage')  # 登出后重定向到首页或其他页面

def usr_home(request):
    store = Shop.objects.filter(owner=request.user, is_approved=True).first()
    return render(request,'usrhome.html',{'store':store})
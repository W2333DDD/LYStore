from django.shortcuts import render

# Create your views here.


def firstpage_show(request):
    return render(request, 'imitatejd.html')


def usr_login(request):
    return render(request,'usr_logoin.html')





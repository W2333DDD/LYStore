from django.http import HttpResponse
from django.shortcuts import render

from .forms import CommentForm
from .models import Comment
from .forms import CommentForm
# Create your views here.



def sub_comment(request):
    if request.method == 'GET':
        form=CommentForm()
        return render(request,'commentsub.html',{'form':form})
    elif request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=Comment()
            comment.text=form.cleaned_data['text']
            comment.image=form.cleaned_data['image']
            comment.video=form.cleaned_data['video']
            comment.save()
        return HttpResponse('评论成功')

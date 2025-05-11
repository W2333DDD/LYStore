from django.forms import Form

from commnents.models import Comment


class CommentForm(Form):
    class Meta:
        model = Comment
        fields = '__all__'
from django import forms
from blog.models import Comment

class CommentForm(forms.ModelForm):
    comment = forms.CharField()

    class Meta:
        model = Comment
        fields = ('comment', )
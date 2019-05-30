from django import forms
from myblog.models import Post


class MyPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'text'
        ]

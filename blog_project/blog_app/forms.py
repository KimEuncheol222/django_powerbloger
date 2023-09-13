from django import forms
from .models import BlogPost

class SearchForm(forms.Form):
    keyword = forms.CharField(label='검색어', max_length=100)


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'topic', 'image']

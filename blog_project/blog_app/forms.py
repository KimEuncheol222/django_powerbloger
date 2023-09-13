from django import forms
from .models import BlogPost
from django_summernote.widgets import SummernoteWidget

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'topic', 'image']
        widgets = {
            'content': SummernoteWidget(),
        }
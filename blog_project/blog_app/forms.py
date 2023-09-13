from django import forms
from .models import BlogPost, Topic
from django_summernote.widgets import SummernoteWidget

class BlogPostForm(forms.ModelForm):
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.RadioSelect,
        to_field_name='name'
    )
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'topic', 'image']
        widgets = {
            'content': SummernoteWidget(),
        }
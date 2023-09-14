from django import forms
from .models import BlogPost, Topic
from django_summernote.widgets import SummernoteWidget

class SearchForm(forms.Form):
    keyword = forms.CharField(label='검색어', max_length=100)


class BlogPostForm(forms.ModelForm):
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.RadioSelect,
        to_field_name='name',
        initial = '일상'
    )
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'topic', 'image']
        widgets = {
            'content': SummernoteWidget(),
        }
        exclude = ['author', 'created_at', 'updated_at', 'is_draft']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

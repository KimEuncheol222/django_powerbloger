from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(label='검색어', max_length=100)

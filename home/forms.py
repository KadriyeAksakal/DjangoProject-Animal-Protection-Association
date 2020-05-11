from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)  #query nesnesi ekledim form da böyle bir şey olmadığı için

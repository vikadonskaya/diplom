from django import forms

from www.models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['photo', 'name', 'description', 'price', 'quantity', 'category', 'brand']


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']

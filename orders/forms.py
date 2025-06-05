from django import forms

from www.models import *
from .models import Address, Card

class OrderForm(forms.Form):
    address = forms.ModelChoiceField(queryset=Address.objects.none())
    card = forms.ModelChoiceField(queryset=Card.objects.none())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].queryset = Address.objects.filter(user=user)
        self.fields['card'].queryset = Card.objects.filter(user=user)



class OrderOneForm(forms.Form):
    address = forms.ModelChoiceField(queryset=Address.objects.none(), label='Адрес')
    card = forms.ModelChoiceField(queryset=Card.objects.none(), label='Карта')
    quantity = forms.IntegerField(min_value=1, initial=1, label='Количество')

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['address'].queryset = Address.objects.filter(user=user)
            self.fields['card'].queryset = Card.objects.filter(user=user)




class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['number', 'code', 'date_cart']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']  # Поля, которые должны отображаться в форме
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваш комментарий'}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),  # Рейтинг от 1 до 5
        }


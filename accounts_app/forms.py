from django import forms
from producto_app.models import ReviewsAmazonDataset



class LoginForm(forms.ModelForm):
    class Meta:
        model = ReviewsAmazonDataset
        fields = ['reviewername','reviewerid',]

    labels = {'reviewername': 'Nombre','reviewerid': 'ID',}

    widgets = {
        'reviewername': forms.TextInput(attrs={'class': 'form-control'}),
        'reviewerid': forms.TextInput(attrs={'class': 'form-control'}),
    }

class RegistroForm(forms.ModelForm):
    class Meta:
        model = ReviewsAmazonDataset
        fields = ['reviewername','reviewerid','asin']

    labels = {'reviewername': 'Nombre','reviewerid': 'ID','asin':'Asin',}

    widgets = {
        'reviewername': forms.TextInput(attrs={'class': 'form-control'}),
        'reviewerid': forms.TextInput(attrs={'class': 'form-control'}),
        'asin': forms.TextInput(attrs={'class': 'form-control'}),
    }

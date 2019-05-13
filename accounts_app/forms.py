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

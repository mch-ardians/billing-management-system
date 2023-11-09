from django import forms
from client.custom_select import ClientCustomSelect
from client.models import Client

class FormProduct(forms.Form):
    nama_product = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nama Produk',
            }
        ),
        label='Nama Produk',
        required=True,
    )
    
    type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Select Type',
            }
        ),
        label='Type',
        required=True,
    )
    
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ClientCustomSelect(attrs={'class': 'form-control choices-single'}),
        label='Client:',
        required=True
    )
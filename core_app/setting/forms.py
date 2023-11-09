from django import forms
from client.models import Client
from product.models import Product
from product.custom_select import ProductCustomSelect
from client.custom_select import ClientCustomSelect

class FormSetting(forms.Form):
    notif_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'Date',
            }
        ),
        label='Date:', 
        required=True,
    )
    
    notif_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control flatpickr-time', 'placeholder': 'HH : MM'}),
        label='Time:',
    )
    
    notif_text = forms.CharField(
        max_length=100,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '*Dear Admin, its invoice time for....', 'rows': 5}),
        label='Text:'
    )
    
    checkbox_email = forms.BooleanField(required=False)
    checkbox_telp = forms.BooleanField(required=False)
    
    email_check = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'})
    )
    
    telp_check = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+6299999999'})
    )
    
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ClientCustomSelect(attrs={'class': 'form-control choices-single', 'id': 'clients'}),
        label='Client:',
        required=True,
    )
    
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        widget=ProductCustomSelect(attrs={'class': 'form-control choices-single', 'id': 'products'}),
        label='Product:',
        required=True
    )
    
    repeat_notif = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Repeat this notification"
    )
    
    status = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'id': 'status'}
            )
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['product'].queryset = Product.objects.filter(id=product_id)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['product'].queryset = Product.objects.none()
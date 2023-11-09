from django import forms
from client.custom_select import ClientCustomSelect
from product.custom_select import ProductCustomSelect
from client.models import Client
from product.models import Product
from .models import Invoice

class FormInvoice(forms.Form):
    no_invoice = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'No Invoice',
                'id': 'no_invoice'
            }
        ),
        label='No Invoice:',
        required=True,
    )
    
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ClientCustomSelect(attrs={'class': 'form-control choices-single', 'id': 'clients'}),
        label='Client:',
        required=True,
    )
        
    invoice_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'Date',
                'id': 'invoice_date'
            }
        ),
        label='Invoice Date:', 
        required=True,
    )
    
    due_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'Date',
                'id': 'due_date'
            }
        ),
        label='Due Date:', 
        required=True,
    )

class FormClientsProduct(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        widget=ProductCustomSelect(attrs={'class': 'form-control choices-single', 'id': 'products'}),
        label='Product:',
        required=True
    )
    
    item = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input an item',
            }
        ),
        required=True,
    )
    
    qty = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Qty',
            }
        ),
        required=True,
    )
    
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Price',
                'step': '0.01'
            }
        ),
        required=True,
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

class SendInvoiceForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ClientCustomSelect(attrs={'class': 'form-control choices-single', 'id': 'client'}),
        label='Client:',
        required=False
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'GuraGu@gmail.com',
                'id': 'email'
            }
        ),
        label='Email:'
    )
    
    no_wa = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '081428793873',
                'id': 'no_wa'
            }
        ),
        label='No. Telp(WA):'
    )
    
    email_check = forms.BooleanField(
        required=False,  
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    
    whatsapp_check = forms.BooleanField(
        required=False,  
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    
    invoice = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'invoice'}),
        label='Dokumen Invoice:'
    )
    
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '*Dear Admin, it\'s invoice time for....',
                'rows': '3',
                'id': 'message'
            }
        ),
        label='Text:'
    )
    
    def __init__(self, *args, **kwargs):
        invoice_id = kwargs.pop('invoice_id', None)
        super(SendInvoiceForm, self).__init__(*args, **kwargs)

        if invoice_id:
            invoice_client = Invoice.objects.select_related('client').filter(id=invoice_id).get()
            self.fields['client'].queryset = Client.objects.filter(id=invoice_client.client_id)

class DetailInvoiceForm(forms.Form):
    nama_client = forms.CharField(
        label='Nama Client:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )
    
    date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'Date',
                'readonly': 'readonly',
            }
        ),
        label='Date:', 
        required=True,
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }
        ),
        label='Email:'
    )
    
    sub_total = forms.CharField(
        label='Sub Total:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )
    
class PaymentForm(forms.Form):
    payment_date = forms.DateField(
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
    
    payment_report = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'hidden': True, 'id': 'file'}),
        label='Bukti Pembayaran:'
    )
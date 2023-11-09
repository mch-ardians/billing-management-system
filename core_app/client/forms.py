from django import forms

class FormClient(forms.Form):
    nama = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nama',
            }
        ),
        label='Nama:'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }
        ),
        label='Email:'
    )
    
    no_wa = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'No.Telp(WA)',
            }
        ),
        label='No.Telp(WA):'
    )
        
class FormAlamat(forms.Form):
    jalan = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Jalan',
            }
        ),
        label='Alamat:'
    )
        
    provinsi = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-3',
                'placeholder': 'Provinsi',
            }
        ),
        label=''
    )
    
    kota_kab = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3 mt-3',
                'placeholder': 'Kota/Kabupaten',
            }
        ),
        label=''
    )
    
    kode_pos = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kode Pos',
            }
        ),
        label='Kode Pos:'
    )
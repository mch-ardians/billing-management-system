from django import forms

class ProfileForm(forms.Form):
    foto = forms.FileField(widget=forms.ClearableFileInput(attrs={'hidden': True, 'id': 'file', 'required': False}))
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'aizen', 'disabled': 'disabled'})
    )
    full_name = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'full_name', 'placeholder': '', 'disabled': 'disabled'})
    )
    position = forms.CharField(
        label="Position",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'position', 'placeholder': '', 'disabled': 'disabled'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'aizensosuke@gmail.com', 'disabled': 'disabled'})
    )
    no_telp = forms.CharField(
        label="No. Telp(WA)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'no_telp', 'placeholder': '', 'disabled': 'disabled'})
    )
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['foto'].required = False
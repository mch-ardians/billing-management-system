from django import forms

class ClientCustomSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(ClientCustomSelect, self).create_option(name, value, label, selected, index, subindex, attrs)
        if value == "":
            option['attrs'] = {'disabled': True, 'selected': True}
            option["label"] = "Select Client"
        return option
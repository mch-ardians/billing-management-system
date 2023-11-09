from django import forms

class ProductCustomSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(ProductCustomSelect, self).create_option(name, value, label, selected, index, subindex, attrs)
        if value == "":
            option['attrs'] = {'disabled': True, 'selected': True}
            option["label"] = "Select Produk"
        return option
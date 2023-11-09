from django.contrib import admin
from .models import Invoice, ClientsProduct

# Register your models here.
admin.site.register(Invoice)
admin.site.register(ClientsProduct)
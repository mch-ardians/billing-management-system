from django.db import models

# Create your models here.
class Invoice(models.Model):
    invoice_num = models.CharField(max_length=255)
    client = models.ForeignKey('client.Client', on_delete=models.DO_NOTHING, null=True, blank=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Done', 'Done'),
    ]
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default='Pending',
    )

    class Meta:
        db_table = 'invoice' 
        
    def __str__(self):
        return f"{self.invoice_num}"
    
class ClientsProduct(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.DO_NOTHING, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    item = models.CharField(max_length=150)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    class Meta:
        db_table = 'clients_product'
    
    def __str__(self):
        return f"{self.item}"
    
class ClientsPayment(models.Model):
    no_invoice = models.CharField(max_length=255)
    payment_date = models.DateField(blank=True, null=True)
    payment_receipt = models.FileField(blank=True, null=True, upload_to="documents/payment/")
    invoice = models.OneToOneField(Invoice, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'clients_payment'
    
    def __str__(self):
        return f"{self.no_invoice}"
from django.db import models

# Create your models here.
class Product(models.Model):
    nama_product = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    client = models.ForeignKey('client.Client', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.nama_product
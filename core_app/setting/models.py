from django.db import models

# Create your models here.
class Setting(models.Model):
    notif_date = models.DateField(null=True)
    notif_time = models.TimeField(null=True)
    text = models.TextField()
    email = models.CharField(max_length=100)
    telp = models.CharField(max_length=100)
    client = models.ForeignKey('client.Client', on_delete=models.DO_NOTHING, null=True, blank=True)
    product = models.ForeignKey('product.Product', on_delete=models.DO_NOTHING, null=True, blank=True)
    STATUS_CHOICES = [
        ('on', 'on'),
        ('off', 'off'),
    ]
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default='off',
    )
    
    class Meta:
        db_table = 'setting'
    
    def __str__(self):
        return f"{self.text}"

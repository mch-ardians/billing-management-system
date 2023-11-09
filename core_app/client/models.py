from django.db import models

# Create your models here.
class Client(models.Model):
    nama = models.CharField(max_length=255)
    no_wa = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    class Meta:
        db_table = 'client' 

    def __str__(self):
        return self.nama

class Alamat(models.Model):
    provinsi = models.CharField(max_length=255)
    kota_kab = models.CharField(max_length=255)
    jalan = models.CharField(max_length=255)
    kode_pos = models.CharField(max_length=5)
    client = models.OneToOneField(Client, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = 'alamat'

    def __str__(self):
        return f"{self.jalan}, {self.kota_kab}, {self.provinsi}"
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=50)
    no_telp_wa = models.CharField(max_length=13)
    foto = models.ImageField(upload_to="images/profile", blank=True, null=True)
    
    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.full_name
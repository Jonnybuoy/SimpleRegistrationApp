from django.db import models

# Create your models here.
class RegistrationDetails(models.Model):
    fullnames = models.CharField(max_length=255, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.full_names

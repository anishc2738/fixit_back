from django.db import models

class Company(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    email=models.EmailField()
    lat=models.FloatField(null=True, blank=True)
    lon=models.FloatField(null=True, blank=True)
    logo=models.ImageField(upload_to='logos/', null=True, blank=True)
    description=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    
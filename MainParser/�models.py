from django.db import models


class Ad(models.Model):

    sites = [
        ('ci', 'Cian'),
        ('av', 'Avito')
    ]
    
    date = models.DateTimeField()
    site = models.CharField(max_length=2, choices=sites)
    title = models.CharField(max_length=60)
    address = models.CharField(max_length=150)
    price = models.IntegerField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    person = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    
    
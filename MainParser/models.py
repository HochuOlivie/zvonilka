from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


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
    person = models.CharField(max_length=30, blank=True)
    link = models.CharField(max_length=200, default='')
    done = models.BooleanField(default=False)

    tmpDone = models.BooleanField(default=False)


class Profile(models.Model):
    user = AutoOneToOneField(User, on_delete=models.CASCADE)
    calls_amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}, phone: {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def make_right_phone(sender, instance, **kwargs):
    username = instance.username
    username = username.replace('+', '').replace('-', '')
    username = username.replace(' ', '').replace('(', '').replace(')', '')
    if username[0] == '8':
        username = '7' + username[1:]
    instance.username = username

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

    date = models.DateTimeField(auto_now_add=True)
    date_done = models.DateTimeField(null=True)

    site = models.CharField(max_length=2, choices=sites)
    title = models.CharField(max_length=60)
    address = models.CharField(max_length=250)
    price = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    
    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    link = models.CharField(max_length=200, unique=True)
    full_link = models.CharField(max_length=255, default="")

    done = models.BooleanField(default=False)
    tmpDone = models.BooleanField(default=False)
    frontDone = models.BooleanField(default=False)

    no_call = models.BooleanField(default=False)
    is_first = models.BooleanField(null=True)

    focused = models.BooleanField(default=False)

    clearColor = models.BooleanField(default=False)
    views = models.IntegerField(default=0)


class Profile(models.Model):
    user = AutoOneToOneField(User, on_delete=models.CASCADE)
    calls_amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    working = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, phone: {self.user.username}"


# For target calls
class TargetAd(models.Model):
    user = AutoOneToOneField(User, on_delete=models.CASCADE)
    ad = AutoOneToOneField(Ad, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)


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


@receiver(post_save, sender=Ad)
def check_no_call(sender, instance, created, **kwargs):
    if created:
        ads = Ad.objects.filter(phone=instance.phone, noCall=True)
        if ads:
            instance.noCall = True

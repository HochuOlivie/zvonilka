# Generated by Django 4.0.3 on 2022-04-10 01:38

import annoying.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MainParser', '0008_alter_ad_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='frontDone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ad',
            name='noCall',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='working',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='TargetAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField(default=False)),
                ('ad', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, to='MainParser.ad')),
                ('user', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-06 22:37

import annoying.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MainParser', '0002_ad_done_ad_link_alter_ad_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calls_amount', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('user', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

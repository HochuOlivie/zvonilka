# Generated by Django 4.0.10 on 2024-06-15 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainParser', '0018_alter_ad_options_alter_profile_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='subway',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]

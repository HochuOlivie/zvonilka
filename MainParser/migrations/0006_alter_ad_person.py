# Generated by Django 4.0.3 on 2022-04-08 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainParser', '0005_alter_ad_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='person',
            field=models.CharField(max_length=30, null=True),
        ),
    ]

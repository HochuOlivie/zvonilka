# Generated by Django 4.0.7 on 2023-08-27 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainParser', '0015_alter_ad_person'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ad',
            old_name='noCall',
            new_name='no_call',
        ),
    ]

# Generated by Django 4.0.10 on 2024-04-16 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainParser', '0017_remove_profile_calls_amount_profile_is_priority_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ad',
            options={'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
        migrations.AlterModelOptions(
            name='targetad',
            options={'verbose_name': 'Точечное объявление', 'verbose_name_plural': 'Точечные объявления'},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='working',
        ),
    ]
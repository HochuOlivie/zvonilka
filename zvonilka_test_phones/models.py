from django.db import models

from MainParser.models import Profile


class PhoneTest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    test_phone = models.CharField(max_length=20, verbose_name='Тестовый номер')

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return f"Тестовый звонок #{self.id} - {self.test_phone}"


class TestCall(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата звонка')
    date_done = models.DateTimeField(null=True)
    person_name = models.CharField(max_length=255, verbose_name='Имя')
    person_phone = models.CharField(max_length=255, verbose_name='Номер')
    phone_test = models.ForeignKey(PhoneTest, on_delete=models.CASCADE, verbose_name='Тест')

    def __str__(self):
        return f""

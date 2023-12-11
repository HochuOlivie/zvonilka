import os
import logging
from datetime import datetime, timedelta
from MainParser.models import Ad
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Удаление старых записей и логирование'

    def handle(self, *args, **options):
        # Количество записей, которые нужно оставить
        keep_records = 20000

        # Удаляем старые записи
        deleted_records = self.delete_old_records(keep_records)

        # Логирование удаления в файл
        log_message = f'{deleted_records} записей удалено. Оставлено {Ad.objects.count()} самых новых записей.'
        self.log_to_file(log_message)

        self.stdout.write(self.style.SUCCESS('Задача успешно выполнена.'))

    def delete_old_records(self, keep_records):
        # Определение даты, на которую нужно оставить записи
        date_threshold = datetime.now() - timedelta(days=30)  # Например, оставим записи за последний месяц

        # Получение записей для удаления
        records_to_delete = Ad.objects.filter(date__lt=date_threshold)

        # Сортировка записей по дате создания в порядке убывания и удаление лишних
        deleted_records = 0
        for record in records_to_delete.order_by('-date')[keep_records:]:
            record.delete()
            deleted_records += 1

        return deleted_records

    def log_to_file(self, message):
        # Создание папки logs, если она не существует
        logs_folder = 'logs'
        os.makedirs(logs_folder, exist_ok=True)

        # Формирование имени файла лога в формате logs/info-<date>.log
        log_file_name = f'info-{datetime.now().strftime("%Y-%m-%d")}.log'
        log_file_path = os.path.join(logs_folder, log_file_name)

        # Настройка логирования
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

        # Запись сообщения в лог
        logging.info(message)

# Запуск скрипта из кода
if __name__ == '__main__':
    command = Command()
    command.handle()

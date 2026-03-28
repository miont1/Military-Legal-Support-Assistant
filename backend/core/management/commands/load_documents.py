from django.core.management.base import BaseCommand
import json
import os
from django.conf import settings
from core.models import LegalDocument

class Command(BaseCommand):
    help = 'Завантажує документи з documents.json у базу даних PostgreSQL (core_legaldocument)'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'documents.json')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Файл не знайдено: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            documents = json.load(f)

        created_count = 0
        updated_count = 0

        for doc_data in documents:
            # Зберігаємо у форматі JSON
            obj, created = LegalDocument.objects.update_or_create(
                title=doc_data.get('title'),
                defaults={
                    'content': doc_data.get('content', ''),
                    'source_url': doc_data.get('source_url', ''),
                    'raw_data': doc_data
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Успішно завантажено документи. Створено: {created_count}, Оновлено: {updated_count}.'
        ))

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    MILITARY_STATUS_CHOICES = [
        ('Мобілізований', 'Мобілізований'),
        ('Контрактник', 'Контрактник'),
        ('Строковик', 'Строковик'),
        ('Офіцер', 'Офіцер'),
        ('Звільнений', 'Звільнений'),
        ('Ветеран', 'Ветеран'),
        ('Член родини', 'Член родини'),
        ('Курсант', 'Курсант'),
    ]
    SERVICE_TYPE_CHOICES = [
        ('ЗСУ', 'ЗСУ'),
        ('НГУ', 'НГУ'),
        ('ТрО', 'ТрО'),
        ('ДПСУ', 'ДПСУ'),
        ('ССО', 'ССО'),
        ('Поліція', 'Поліція'),
        ('Нацгвардія', 'Нацгвардія'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    military_status = models.CharField(max_length=50, choices=MILITARY_STATUS_CHOICES)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.military_status}"

class LegalDocument(models.Model):
    """
    Represents a legal document (law, order, statute) chunk.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    source_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ChatSession(models.Model):
    """
    Represents a chat session containing multiple queries.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class UserQuery(models.Model):
    """
    Stores the history of user questions and AI responses.
    """
    DOCUMENT_STATUS_CHOICES = [
        ('Є всі документи', 'Є всі документи'),
        ('Документи відсутні', 'Документи відсутні'),
        ('Є лише рапорт', 'Є лише рапорт'),
        ('Часткові документи', 'Часткові документи'),
        ('Є висновок ВЛК', 'Є висновок ВЛК'),
        ('Є наказ', 'Є наказ'),
    ]
    SITUATION_STAGE_CHOICES = [
        ('Ситуація тільки виникла', 'Ситуація тільки виникла'),
        ('Рапорт подано', 'Рапорт подано'),
        ('Отримано відмову', 'Отримано відмову'),
        ('Службове розслідування', 'Службове розслідування'),
        ('Досудовий етап', 'Досудовий етап'),
        ('Судовий розгляд', 'Судовий розгляд'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='queries')
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, null=True, blank=True, related_name='queries')
    query_text = models.TextField()
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New metadata fields
    issue_category = models.CharField(max_length=100, blank=True, null=True)
    document_status = models.CharField(max_length=50, choices=DOCUMENT_STATUS_CHOICES, blank=True, null=True)
    situation_stage = models.CharField(max_length=50, choices=SITUATION_STAGE_CHOICES, blank=True, null=True)
    sources = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Query at {self.created_at}"

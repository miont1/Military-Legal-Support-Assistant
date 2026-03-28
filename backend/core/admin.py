from django.contrib import admin
from .models import UserProfile, LegalDocument, ChatSession, UserQuery

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'military_status', 'service_type')
    search_fields = ('user__username', 'user__email')
    list_filter = ('military_status', 'service_type')

@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'user__username')
    list_filter = ('created_at',)

@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session', 'issue_category', 'created_at')
    search_fields = ('query_text', 'response_text', 'user__username')
    list_filter = ('issue_category', 'document_status', 'situation_stage', 'created_at')

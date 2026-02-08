from django.urls import path
from .views import LegalChatView, RegistrationView, ChatSessionListView, ChatSessionDetailView, UserProfileView, ChangePasswordView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('chat/', LegalChatView.as_view(), name='legal-chat'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('sessions/', ChatSessionListView.as_view(), name='session-list'),
    path('sessions/<int:pk>/', ChatSessionDetailView.as_view(), name='session-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

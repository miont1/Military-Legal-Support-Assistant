from django.urls import path
from .views import LegalChatView, RegistrationView, ChatSessionListView, ChatSessionDetailView, UserProfileView, ChangePasswordView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny

class LoginView(ObtainAuthToken):
    authentication_classes = []
    permission_classes = [AllowAny]

urlpatterns = [
    path('chat/', LegalChatView.as_view(), name='legal-chat'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='api_token_auth'),
    path('sessions/', ChatSessionListView.as_view(), name='session-list'),
    path('sessions/<int:pk>/', ChatSessionDetailView.as_view(), name='session-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

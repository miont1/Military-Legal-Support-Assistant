from .models import UserQuery, ChatSession
from .serializers import RegistrationSerializer, QuestionSerializer, UserQuerySerializer, ChatSessionSerializer, UserUpdateSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import LegalAssistantService

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Registration Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ChatSessionListView(generics.ListAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).order_by('-created_at')

class ChatSessionDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = UserQuerySerializer
    permission_classes = [IsAuthenticated]
    queryset = ChatSession.objects.all()

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        session = self.get_object()
        queries = session.queries.all().order_by('created_at')
        serializer = UserQuerySerializer(queries, many=True)
        return Response(serializer.data)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                return Response({'status': 'password set'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LegalChatView(APIView):
    """
    API View to handle user queries for legal advice.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            query_text = serializer.validated_data['question']
            session_id = serializer.validated_data.get('session_id')
            
            metadata = {
                'issue_category': serializer.validated_data.get('issue_category'),
                'document_status': serializer.validated_data.get('document_status'),
                'situation_stage': serializer.validated_data.get('situation_stage'),
            }
            

            user_profile = None
            if request.user.is_authenticated:
                try:
                    user_profile = request.user.profile
                except:
                    pass


            session = None
            if request.user.is_authenticated:
                if session_id:
                    session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
                else:

                    title = query_text[:50] + "..." if len(query_text) > 50 else query_text
                    session = ChatSession.objects.create(user=request.user, title=title)

            service = LegalAssistantService()

            result = service.process_query(query_text, metadata, user_profile, user=request.user, session=session)
            

            if session:
                result['session_id'] = session.id
                result['session_title'] = session.title

            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

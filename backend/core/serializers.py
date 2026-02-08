from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserQuery, UserProfile, ChatSession

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['military_status', 'service_type']

class RegistrationSerializer(serializers.ModelSerializer):
    military_status = serializers.ChoiceField(choices=UserProfile.MILITARY_STATUS_CHOICES, write_only=True)
    service_type = serializers.ChoiceField(choices=UserProfile.SERVICE_TYPE_CHOICES, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'military_status', 'service_type']

    def create(self, validated_data):
        military_status = validated_data.pop('military_status')
        service_type = validated_data.pop('service_type')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        UserProfile.objects.create(
            user=user,
            military_status=military_status,
            service_type=service_type
        )
        return user

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'created_at']

class UserQuerySerializer(serializers.ModelSerializer):
    """
    Serializer for the UserQuery model.
    """
    class Meta:
        model = UserQuery
        fields = ['id', 'query_text', 'response_text', 'created_at', 'issue_category', 'document_status', 'situation_stage', 'sources']
        read_only_fields = ['response_text', 'created_at']

class QuestionSerializer(serializers.Serializer):
    """
    Serializer for the incoming question.
    """
    question = serializers.CharField(required=True, max_length=1000)
    session_id = serializers.IntegerField(required=False, allow_null=True)
    issue_category = serializers.CharField(required=False, allow_blank=True, max_length=100)
    document_status = serializers.ChoiceField(choices=UserQuery.DOCUMENT_STATUS_CHOICES, required=False, allow_blank=True)
    situation_stage = serializers.ChoiceField(choices=UserQuery.SITUATION_STAGE_CHOICES, required=False, allow_blank=True)

class UserUpdateSerializer(serializers.ModelSerializer):
    military_status = serializers.CharField(source='profile.military_status')
    service_type = serializers.CharField(source='profile.service_type')

    class Meta:
        model = User
        fields = ['username', 'email', 'military_status', 'service_type']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        military_status = profile_data.get('military_status')
        service_type = profile_data.get('service_type')

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()


        if hasattr(instance, 'profile'):
            profile = instance.profile
        else:
            profile = UserProfile.objects.create(user=instance)

        if military_status:
            profile.military_status = military_status
        if service_type:
            profile.service_type = service_type
        profile.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

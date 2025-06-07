from rest_framework import serializers

from .models import User, SMSVerification


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={'required': 'Необходимо указать email.'}
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'is_active',
            'is_staff',
            'image',
        ]

    def validate_email_exists(self, value):
        """
        Если пользователь уже существует, просто пропускаем проверку.
        """
        if User.objects.filter(email=value).exists():
            return value
        return value


class SMSVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSVerification
        fields = [
            'id',
            'email',
            'code',
            'created_at',
            'is_used',
        ]

    def validate(self, attrs):
        if not attrs.get('email'):
            raise serializers.ValidationError({'email': 'Необходимо указать email.'})
        if not attrs.get('code'):
            raise serializers.ValidationError({'code': 'Необходимо ввести код.'})
        return attrs
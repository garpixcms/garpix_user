from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string
from rest_framework import serializers


User = get_user_model()

try:
    Config = import_string(settings.GARPIX_USER_CONFIG)
    MIN_LENGTH_PASSWORD = Config.get_solo().min_length_password
    MIN_DIGITS_PASSWORD = Config.get_solo().min_digits_password
    MIN_CHARS_PASSWORD = Config.get_solo().min_chars_password
    MIN_UPPERCASE_PASSWORD = Config.get_solo().min_uppercase_password
except Exception:
    MIN_LENGTH_PASSWORD = getattr(settings, 'MIN_LENGTH_PASSWORD', 8)
    MIN_DIGITS_PASSWORD = getattr(settings, 'MIN_DIGITS_PASSWORD', 2)
    MIN_CHARS_PASSWORD = getattr(settings, 'MIN_CHARS_PASSWORD', 2)
    MIN_UPPERCASE_PASSWORD = getattr(settings, 'MIN_UPPERCASE_PASSWORD', 1)


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)

    def validate(self, data):
        min_length = MIN_LENGTH_PASSWORD
        min_digits = MIN_DIGITS_PASSWORD
        min_chars = MIN_CHARS_PASSWORD
        min_uppercase = MIN_UPPERCASE_PASSWORD

        queryset = User.objects.filter(email=data['email']).first()
        if queryset is not None:
            raise serializers.ValidationError("This email is already in use")

        # check for 2 min length
        if len(data['password']) < min_length:
            raise serializers.ValidationError(
                'Password must be at least {min_length} characters long.'.format(min_length=min_length)
            )

        # check for 2 digits
        if sum(c.isdigit() for c in data['password']) < min_digits:
            raise serializers.ValidationError(
                'Password must container at least {min_digits} digits.'.format(min_digits=min_digits)
            )

        # check for 2 char
        if sum(c.isalpha() for c in data['password']) < min_chars:
            raise serializers.ValidationError(
                'Password must container at least {min_chars} chars.'.format(min_chars=min_chars)
            )

        # check for uppercase letter
        if sum(c.isupper() for c in data['password']) < min_uppercase:
            raise serializers.ValidationError(
                'Password must container at least {min_uppercase} uppercase letter.'.format(min_uppercase=min_uppercase)
            )

        # check for password = password_2
        if data['password'] != data['password_2']:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )

        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_2',)

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth.serializers import RestoreCommonSerializer, RestoreByEmailSerializer, \
    RestoreSetPasswordByEmailSerializer, RestoreCheckCodeByEmailSerializer

User = get_user_model()


class RestoreEmailPasswordViewSet(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return RestoreByEmailSerializer
        if self.action == 'check_code':
            return RestoreCheckCodeByEmailSerializer
        return RestoreSetPasswordByEmailSerializer

    @extend_schema(summary='Восстановление пароля по email. Этап 1')
    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        serializer = RestoreByEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = User().send_restore_code(email=serializer.data['email'])

        if not result['result']:
            raise serializers.ValidationError(result['message'])
        return Response(result)

    @extend_schema(summary='Восстановление пароля по email. Этап 2')
    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        serializer = RestoreCheckCodeByEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = User().check_restore_code(email=serializer.data['email'],
                                           confirmation_code=serializer.data['confirmation_code'])

        if not result['result']:
            raise serializers.ValidationError(result['message'])
        return Response(result)

    @extend_schema(summary='Восстановление пароля по email. Этап 3')
    @action(methods=['POST'], detail=False)
    def set_password(self, request, *args, **kwargs):

        serializer = RestoreSetPasswordByEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = User().restore_password(email=serializer.data['email'], token=serializer.data['token'],
                                         new_password=serializer.data['new_password'])

        if not result['result']:
            raise serializers.ValidationError(result['message'])
        return Response(result)

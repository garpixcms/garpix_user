from user.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth.serializers import RestoreByPhoneSerializer, RestoreSetPasswordByPhoneSerializer, \
    RestoreCheckCodeByPhoneSerializer


class RestorePhonePasswordViewSet(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return RestoreByPhoneSerializer
        if self.action == 'check_code':
            return RestoreSetPasswordByPhoneSerializer
        return RestoreSetPasswordByPhoneSerializer

    @extend_schema(summary='Восстановление пароля по phone. Этап 1')
    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        serializer = RestoreByPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = User().send_restore_code(phone=serializer.data['phone'])

        if not result['result']:
            raise serializers.ValidationError(result['message'])
        return Response(result)

    @extend_schema(summary='Восстановление пароля по phone. Этап 2')
    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        serializer = RestoreCheckCodeByPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = User().check_restore_code(phone=serializer.data['phone'],
                                           confirmation_code=serializer.data['confirmation_code'])

        if not result['result']:
            raise serializers.ValidationError(result['message'])
        return Response(result)

    @extend_schema(summary='Восстановление пароля по phone. Этап 3')
    @action(methods=['POST'], detail=False)
    def set_password(self, request, *args, **kwargs):

        serializer = RestoreSetPasswordByPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = User().restore_password(phone=serializer.data['phone'], token=serializer.data['token'],
                                         new_password=serializer.data['new_password'])

        if not result['result']:
            raise serializers.ValidationError(result['message'])
        return Response(result)

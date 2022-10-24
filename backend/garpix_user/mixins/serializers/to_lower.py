from rest_framework import serializers


class ToLowerMixin(serializers.Serializer):

    def validate_email(self, value):
        """
        ensure that email is always lower case.
        """
        return value.lower()

    def validate_username(self, value):
        """
        ensure that username is always lower case.
        """
        return value.lower()

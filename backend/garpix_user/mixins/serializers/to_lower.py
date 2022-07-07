from rest_framework import serializers


class ToLowerMixin(serializers.Serializer):

    def validate_email(self, value):
        """
        ensure that email is always lower case.
        """
        return value.lower()

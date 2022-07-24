from rest_framework import serializers

from account.models import Account


class AccountSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password', 'nickname']
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True, "required": True}
        }

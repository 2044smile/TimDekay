from rest_framework import serializers

from account.models import Account
from phonenumber_field.serializerfields import PhoneNumberField


class AccountSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password', 'nickname']
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True, "required": True}
        }


class AccountPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone']
        extra_kwargs = {
            "phone": {"required": True},
        }

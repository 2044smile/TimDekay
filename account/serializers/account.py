from rest_framework import serializers

from account.models import Account
from phonenumber_field.serializerfields import PhoneNumberField


# Model Serialzier 는 수치상으로 매우 느린 편에 속하지만, 개인 프로젝트의 경우엔 신경 쓸 필요 없으므로 그냥 사용하였습니다. 참고용
class AccountSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password', 'nickname', 'real_name', 'phone']
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True, "required": True},
            "nickname": {"required": True},
            "real_name": {"required": False},
            "phone": {"required": True}
        }


class AccountPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone']
        extra_kwargs = {
            "phone": {"required": True},
        }


class AccountLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password']
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True, "required": True},
        }


class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {
            "password": {"write_only": True},
        }


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['pk', 'password']

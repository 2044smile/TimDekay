from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, permissions, mixins

from account.models.account import Account
from account.serializers.account import AccountSignUpSerializer


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_id='회원가입',
    operation_description='계정을 생성합니다.',
    tags=['Account']
))
class AccountSignUpViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Account.objects.all()
    serializer_class = AccountSignUpSerializer

    def get_serializer_context(self):
        if self.action == 'create':
            return AccountSignUpSerializer



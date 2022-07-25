from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models.account import Account, UserManager
from account.serializers.account import AccountSignUpSerializer, AccountPhoneNumberSerializer


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


@swagger_auto_schema(
    method='post',
    request_body=AccountPhoneNumberSerializer,
    operation_id="전화번호 인증",
    responses={
        200: 'OK'
    },
    tags=['Account']
)
@api_view(['POST'])
def account_phone(request):
    serializer = AccountPhoneNumberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data)

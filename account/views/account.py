from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

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

    def create(self, request, *args, **kwargs):
        if not cache.get('phone'):
            raise ValueError("not have cache data")
        else:
            validate_phone = cache.get('phone')
            try:
                queryset = Account.objects.create_user(
                    email=request.data['email'],
                    password=request.data['password'],
                    nickname=request.data['nickname'],
                    real_name=request.data['real_name'],
                    phone=validate_phone
                )
            except ValueError:
                raise ValueError('폰 번호가 중복되었거나, 닉네임이 중복되었거나, 이메일이 중복 된 경우')
            return Response({"data": "data"})  # FIXME: Here


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

    validate_phone = serializer.data['phone']
    cache.set('phone', validate_phone, timeout=180)

    return Response(serializer.data)

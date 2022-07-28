from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework import viewsets, mixins
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models.account import Account, UserManager
from account.serializers.account import AccountSignUpSerializer, AccountPhoneNumberSerializer, AccountLoginSerializer, \
    AccountInfoSerializer, PasswordResetSerializer


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

            serializer = AccountSignUpSerializer(queryset)

            return Response(data=serializer.data)


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


class AccountLoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(
        operation_id="로그인",
        request_body=AccountLoginSerializer,
        tags=['Account'],
    )
    def post(self, request):
        user = Account.objects.get(email=request.data['email'])  # 이메일이 없으면 알아서 에러 발생

        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        res = Response(
            {
                "user": user.email,
                "message": "login success",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
        )
        return res


class AccountInfoView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(
        operation_id="내정보",
        request_query=AccountInfoSerializer,
        tags=['Account'],
    )
    def get(self, request, pk):
        instance = Account.objects.get(pk=pk)
        serializer = AccountInfoSerializer(instance)
        data = serializer.data

        return Response(data)


class PasswordResetView(UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Exception as e:
            return Response({'message': e})

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = self.serializer_class(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response(serializer.data)
        return Response({'message': True})

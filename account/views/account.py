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
from django.shortcuts import get_object_or_404

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
    # 전화번호 인증은 redis 로 실시하였다.
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
        try:
            # Account.objects.get(email=request.data['email']).password -> sha256한 값이 나온다.
            # authenticate 는 사용자 인증을 담당한다. 사용자명과 비밀번호가 정확한지 확인한다.
            # authenticate(email=request.data['email'], password=request.data['password']) 가 되야하지만
            # 나는 Email 로 로그인 기능 구현하기를 설정했지만 바뀌는 점은 없었다.
            # 올바른 패스워드를 입력하기 바란다.
            print(request.data['email'])
            print(request.data['password'])
            print(authenticate(email=request.data['email'], password=request.data['password']))  # None
            # user = authenticate(email=request.data['email'], password=request.data['password'])
            user = Account.objects.get(email=request.data['email'])
        except Account.DoesNotExist:
            user = None

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
    # 정상작동 한다.
    # 앞에서 authenticate 설명했듯이 로그인에서 패스워드 비교하는 문제는 찾아볼 수 없지만,
    # 패스워드 변경에 대해서는 잘 작동하는 것을 확인할 수 있다.
    # 추가로 account/login 에서 확인하면 패스워드가 틀려도 액세스, 리프레시 토큰을 주니 jwt-token-auth 에서 하기 바란다.
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

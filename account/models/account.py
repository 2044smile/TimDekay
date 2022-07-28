from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.cache import cache

from account.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField
import random


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, real_name, password, phone=None):  # real_name null=True
        if not email:
            raise ValueError('Users must have an email address')
        if not cache.get('phone'):
            raise ValueError('Users must have an phone')

        user = self.model(
            email=UserManager.normalize_email(email),
            nickname=nickname,
            real_name=real_name,  # 이름
            phone=cache.get('phone'),
        )
        user.set_password(password)
        user.is_certified = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, nickname, password):
        user = self.model(
            email=email,
            nickname=nickname,
        )
        user.set_password(password)
        user.is_admin = True
        # create_superuser 를 할 때 self 의 model 이 기본적으로 등록 된 데이터페이스를 보는 것 같습니다.
        # 기본적으로 만들어진 phone 의 조건은 unique=True 어드민 계정을 생성할 때 사용되는 것은 create_superuser 이지만
        # 관련이 있는 걸로 확인하였고, 아래의 구문을 추가하였습니다. + 어드민 계정을 만드는 경우에 돌아가는 코드이기 때문에
        # 중복으로 인한 에러를 발견하기 어려울 것 입니다.
        lst = random.sample(range(1, 55), 5)  # I don't know create_superuser
        user.phone = "+" + str(lst)
        user.save(using=self._db)

        return user


class Account(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='email'
    )
    nickname = models.CharField(
        max_length=16,
        blank=False,
        unique=True,
        verbose_name='닉네임'
    )
    real_name = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )
    phone = PhoneNumberField(
        max_length=13,
        blank=False,
        unique=True,
        verbose_name='전화 번호'
    )
    is_active = models.BooleanField(default=True)
    is_certified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Does the user have a specific permission?
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Does the user have permissions to view the app `app_label`?
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # Is the user a member of staff?
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = '유저들'  # verbose_name_plural Permission(models.Model)
        ordering = ['-created_at']

    def __str__(self):
        return self.email


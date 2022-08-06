# 프로젝트명 TimDekay
## 사용한 라이브러리
### Python 3.10+, Django, phonenumber-field, drf-simplejwt, drf-yasg(swagger)

## 사용한 기술
### redis
#### redis를 사용하기 위해서는 redis와 django-redis를 설치하셔야 합니다.
1. brew install redis 
2. redis-server
3. https://github.com/jazzband/django-redis/tags
4. pip install django-redis
Window Ubuntu
1. sudo apt install redis
2. sudo service redis-server start

## 실행 방법
1. redis를 설치하셨다면 'redis-server'
2. python manage.py makemigrations
3. python manage.py migrate
4. python manage.py runserver
5. http://127.0.0.1:8000/swagger/

## 진행 순서
1. account/phone 휴대폰 인증 (정상 작동)
2. account/create 회원가입 (정상 작동)
3. <span style="color:red">account/login 로그인 --> access, refresh token 생성 **AccessToken 복사**
 로그인 authenticate가 안되는 문제가 발생 comment 를 확인 (문제 발생)</span>
4. account/info/{id} 내정보 --> id는 1을 입력, Swagger 자물쇠 버튼을 눌러 JWT (AccessToken) 입력 (정상 작동)
5. account/password/reset/{id} --> id는 1을 입력, 변경하고 싶은 패스워드 입력 (정상 작동)

## 앞으로의 진행 사항

1. 할 수 있다
2. 할 수 있다
3. 할 수 있다
4. 할 수 있다
5. 할 수 있다
6. authenticate 문제

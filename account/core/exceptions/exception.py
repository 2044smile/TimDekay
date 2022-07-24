from rest_framework.exceptions import APIException


class SignUpBadRequest(APIException):
    status_code = 400
    default_detail = "잘못된 요청입니다."


class SignUpNotFound(APIException):
    status_code = 404
    default_detail = "요청한 페이지를 찾을 수 없습니다."

from rest_framework.exceptions import APIException


# 해당 부분은 사용하려고 만들어뒀지만 개인 프로젝트에서는 딱히 필요가 없다고 느껴서 진행하지 않았습니다.
# 회사의 경우엔 꼭 꼭 꼭 처리해야 될 것으로 보여집니다.
class SignUpBadRequest(APIException):
    status_code = 400
    default_detail = "잘못된 요청입니다."


class SignUpNotFound(APIException):
    status_code = 404
    default_detail = "요청한 페이지를 찾을 수 없습니다."

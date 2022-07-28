from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@swagger_auto_schema(
    method='get',
    operation_id="health_check",
    responses={
        200: 'OK'
    },
    tags=['HealthCheck']
)
@api_view(['GET'])
def health_check(request):
    """
    :param request:
    :return: health check SUCCESS

    Kubernetes 를 이용하여 서버를 띄울 시 Readiness, Liveness, Startup 등을 설정해야하고,
    Pod 에서 수시로 현재 서버가 정상적인지 Request 를 보낸다.

    기본적으로 하나 있으면 여러 방면에 사용 할 수 있음을 강조
    """
    response = {
        'status': 'health check SUCCESS'
    }
    return Response(response, status=status.HTTP_200_OK)

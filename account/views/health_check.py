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
    tags=['health-check']
)
@api_view(['GET'])
def health_check(request):
    response = {
        'status': 'health check SUCCESS'
    }
    return Response(response, status=status.HTTP_200_OK)

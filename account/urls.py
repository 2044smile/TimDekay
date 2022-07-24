from django.urls import path

from . import views

urlpatterns = [
    path('health_check', views.health_check),
    path('account/create', views.AccountSignUpViewSet.as_view({'post': 'create'}))
]

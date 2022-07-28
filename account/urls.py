from django.urls import path

from . import views

urlpatterns = [
    path('health_check', views.health_check),
    path('account/phone', views.account_phone),
    path('account/create', views.AccountSignUpViewSet.as_view({'post': 'create'})),
    path('account/login', views.AccountLoginView.as_view()),
    path('account/info/<int:pk>', views.AccountInfoView.as_view()),
    path('account/password/reset/<int:pk>', views.PasswordResetView.as_view())
]

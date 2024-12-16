from django.urls import path
from api.views import RegisterView, LoginView, GetUserView, UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Endpoint untuk registrasi dan login kustom
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # Endpoint untuk autentikasi berbasis SimpleJWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', GetUserView.as_view(), name='user'),
    path('users/', UserListView.as_view(), name='users'),
]

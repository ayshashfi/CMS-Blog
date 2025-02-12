from django.urls import path
from .views import TokenObtainPairView, TokenRefreshView,RegisterView, CustomTokenObtainPairView, LogoutView,AdminLoginAPIView,UserDetailView


urlpatterns = [
   
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),  # This will provide the access and refresh tokens
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/login/', AdminLoginAPIView.as_view(), name='admin-login'),
]

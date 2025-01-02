from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer  # Import the serializer here
from django.contrib.auth import authenticate


# Custom Token Refresh View
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


# Register API: Create a new user
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Custom Token Obtain Pair View to include additional claims
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response

    def validate(self, attrs):
        data = super().validate(attrs)
        data["is_superuser"] = self.user.is_superuser  # Add is_superuser field to payload
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add additional claims to the token
        token['is_superuser'] = user.is_superuser  # Include is_superuser in the token
        return token


# Logout API: Blacklist the refresh token
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            # Extract the refresh token from the request
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a RefreshToken instance and blacklist it
            token = RefreshToken(refresh_token)
            token.blacklist()  # Optionally blacklist the refresh token

            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


# Admin Login API: Authenticate user and issue JWT tokens
class AdminLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to access the login API

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user using email and password
        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_staff:
            # Create JWT tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'message': 'Login successful',
                'role': 'admin'
            })

        return Response({
            'message': 'Invalid credentials or not an admin.'
        }, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.permissions import IsAuthenticated

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(data)




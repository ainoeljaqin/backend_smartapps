from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import UserSerializer

# Custom User model
User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        is_staff = request.data.get('is_staff', False)

        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = is_staff
        user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
            "access": access_token,
            "refresh": str(refresh),
            "is_staff": user.is_staff,
            }, status=status.HTTP_200_OK)

class GetUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)
    
class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

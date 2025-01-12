from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer, UserLoginSerializer
from rest_framework.response import Response
from user.models import User
from rest_framework.decorators import action, authentication_classes
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def test(self, request):
        queryset = self.get_queryset()
        self.serializer_class = UserSerializer(queryset, many=True)
        return Response(self.serializer_class.data)

class UserRegistrationView(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def create(self, request):
        from django.contrib.auth import authenticate


        username = request.data.get('username')
        password = request.data.get('password')

        user_auth = authenticate(username=username, password=password)

        if user_auth is not None:
            refresh = RefreshToken.for_user(user_auth)
            return Response({
                'token': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': "Invalid credentailas"}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    pass
class AdminUserViewSet(viewsets.ViewSet):
    pass
class AuthenticationView(APIView):
    pass
class SensitiveDataView(APIView):
    pass
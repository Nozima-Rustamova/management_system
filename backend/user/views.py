'''Views for the user API'''

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, permissions
from .serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    serializer_class=UserSerializer

class ManagerUserView(generics.RetrieveUpdateAPIView):
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]


    def get_object(self):
        return self.request.user

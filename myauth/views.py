from rest_framework.viewsets import ModelViewSet

from myauth.models import User
from myauth.serializers import UserSerializer


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from myauth.models import User
from myauth.serializers import (UserListSerializer,
                                UserDetailSerializer,
                                UserCreateSerializer,
                                UserUpdateSerializer)


class UserViewset(ModelViewSet):
    serializer_class = UserListSerializer
    serializer_map = {
        'list': UserListSerializer,
        'create': UserCreateSerializer,
        'update': UserUpdateSerializer,
        'retrieve': UserDetailSerializer,
        'partial_update': UserUpdateSerializer,
    }

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action in self.serializer_map.keys():
            return self.serializer_map[self.action]
        else:
            return super().get_serializer_class()


# class UserCreateViewSet(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserNestedSerializer
#     permission_classes = [AllowAny]

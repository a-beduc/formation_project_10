from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from myauth.models import User
from myauth.serializers import (UserListSerializer,
                                UserDetailSerializer,
                                UserCreateSerializer,
                                UserUpdateSerializer)

from myauth.permissions import IsAdminAuthenticated, IsOwner


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

    def get_permissions(self):
        if self.action in [
            'retrieve',
            'update',
            'partial_update',
            'destroy',
        ]:
            permission_classes = [IsOwner | IsAdminAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

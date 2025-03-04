from rest_framework.viewsets import ModelViewSet

from myauth.models import User
from myauth.serializers import UserNestedSerializer, UserFullDetailSerializer
from myauth.serializers import (UserListSerializer,
                                UserDetailSerializer,


class UserViewset(ModelViewSet):
    serializer_class = UserNestedSerializer
    detail_serializer_class = UserFullDetailSerializer
    serializer_class = UserListSerializer
    serializer_map = {
        'list': UserListSerializer,
        'retrieve': UserDetailSerializer,
    }

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action in self.serializer_map.keys():
            return self.serializer_map[self.action]
        else:
            return super().get_serializer_class()

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from myauth.serializers import (UserListSerializer,
                                UserDetailSerializer,
                                UserCreateSerializer,
                                UserUpdateSerializer)

from myauth.permissions import IsAdminAuthenticated, IsOwner

User = get_user_model()


class UserViewset(ModelViewSet):
    """
    The SoftDesk API is a RESTful API built using Django Rest Framework with the objective
    to develop a secured and efficient backend interface to serve different front-end applications.
    The API use Json Web Token to define access permissions for the resources.

    The Users resources can be used by users to access their own profiles and edit its content. It may
    also be used to display all the users id and username.

    A filter can be used to ease the search for a specific user id or username.

    If you want to see the list of all the projects, please refer to the [projects endpoint](/api/v1/projects/).
    """
    serializer_class = UserListSerializer
    serializer_map = {
        'list': UserListSerializer,
        'create': UserCreateSerializer,
        'update': UserUpdateSerializer,
        'partial_update': UserUpdateSerializer,
        'retrieve': UserDetailSerializer
    }
    permission_map = {
        'list': [IsAuthenticated],
        'create': [IsAdminAuthenticated]
    }
    view_name_map = {
        'list': 'User List',
        'create': 'User Create',
        'update': 'User Update',
        'partial_update': 'User Update',
        'retrieve': 'User Detail',
        'destroy': 'User Delete',
    }
    default_permission = [IsOwner | IsAdminAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action in self.serializer_map.keys():
            return self.serializer_map[self.action]
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in self.permission_map.keys():
            permission_classes += self.permission_map.get(self.action, [])
        else:
            permission_classes += self.default_permission
        return [permission() for permission in permission_classes]

    def permission_denied(self, request, message=None, code=None):
        message = "Vous n'avez pas la permission d'accéder à cette ressource."
        super().permission_denied(request, message=message, code=code)

    def get_view_name(self):
        action = getattr(self, 'action', None)
        return self.view_name_map.get(action, super().get_view_name())

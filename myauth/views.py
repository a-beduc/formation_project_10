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
    The API uses Json Web Token to define access permissions for the resources.

    The User resource:

    - Allows users to access and edit their own profiles.
    - Allows staff or superusers to manage all user records.
    - Provides basic filtering to search for user IDs or usernames.

    An example of usage:

    - To retrieve a list of all users: GET /api/v1/users/
    - To create a new user (Admin only): POST /api/v1/users/
    - For a specific user: GET /api/v1/users/<pk>/
    - To update a user (partial or full): PATCH or PUT /api/v1/users/<pk>/
    - To delete a user: DELETE /api/v1/users/<pk>/

    If you want to see the list of all the projects, please refer to the [projects endpoint](/api/v1/projects/).
    """
    # Serializers
    serializer_class = UserListSerializer
    serializer_map = {
        'list': UserListSerializer,
        'create': UserCreateSerializer,
        'update': UserUpdateSerializer,
        'partial_update': UserUpdateSerializer,
        'retrieve': UserDetailSerializer
    }

    # Permissions
    default_permission = [IsOwner | IsAdminAuthenticated]
    permission_map = {
        'list': [IsAuthenticated],
        'create': [IsAdminAuthenticated]
    }

    # Custom name in DRF web interface
    view_name_map = {
        'list': 'User List',
        'create': 'User Create',
        'update': 'User Update',
        'partial_update': 'User Update',
        'retrieve': 'User Detail',
        'destroy': 'User Delete',
    }

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        """
        Check for the action performed and if a serializer correspond to the action in serializer_map, return it.
        Otherwise, return a default serializer.
        :return:
        """
        if self.action in self.serializer_map.keys():
            return self.serializer_map[self.action]
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        """
        Return a list of permissions that this view requires. Every resources endpoint need at least the
        [IsAuthenticated] permission.
        """
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
        """
        Modify displayed name of view on DRF web interface.
        """
        action = getattr(self, 'action', None)
        return self.view_name_map.get(action, super().get_view_name())

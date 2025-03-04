from rest_framework.viewsets import ModelViewSet

from myauth.models import User
from myauth.serializers import UserNestedSerializer, UserFullDetailSerializer


class UserViewset(ModelViewSet):
    serializer_class = UserNestedSerializer
    detail_serializer_class = UserFullDetailSerializer

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()

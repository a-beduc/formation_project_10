from django_filters import rest_framework as filters
from myauth.models import User


class UserFilter(filters.FilterSet):
    user_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='iexact')
    username_contains = filters.CharFilter(
        field_name='username',
        lookup_expr='icontains'
    )

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'username_contains'
        ]

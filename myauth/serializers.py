from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from myauth.models import User


class UserFullDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'date_of_birth',
            'can_be_contacted',
            'can_data_be_shared',
            'created_time'
        ]


class UserNestedSerializer(ModelSerializer):
    user_detail = HyperlinkedIdentityField(view_name='user-detail', lookup_field='pk')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'user_detail'
        ]


class UserSummarySerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]

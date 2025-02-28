from rest_framework.serializers import ModelSerializer, ValidationError
from myauth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'date_of_birth',
                  'can_be_contacted',
                  'can_data_be_shared',
                  'created_time'
                  ]

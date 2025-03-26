from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework.serializers import (ModelSerializer,
                                        HyperlinkedIdentityField,
                                        CharField)
from myauth.models import User


class UserDetailSerializer(ModelSerializer):
    """
    Serializer for the User model. Detailed view of a User, including
    all major fields.
    """
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


class UserListSerializer(ModelSerializer):
    """
    Serializer for the User model. Minimal user info + a link to the
    detailed view.
    """
    user_detail = HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='pk'
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'user_detail'
        ]


class UserSummarySerializer(ModelSerializer):
    """
    Serializer for the User model. A short representation of the user
    (id + username).
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]


class UserPostSerializer(ModelSerializer):
    """
    Serializer for the User model. Serializer for creating a new User or
    updating an existing one.
    """
    password = CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'date_of_birth',
            'can_be_contacted',
            'can_data_be_shared',
        ]

    def validate_password(self, password):
        """
        Method to check Django's password constraints and raise a DRF
        ValidationError if not valid.
        """
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise DjangoValidationError(e.messages)
        return password

    def create(self, validated_data):
        """
        Method called when a user is created, hash the password before
        saving it in the database.
        """
        if ('password' not in validated_data.keys() or
                not validated_data['password']):
            raise DRFValidationError(
                {"password": ["Password is required"]}
            )
        plain_password = validated_data.pop('password', None)
        user = super(UserPostSerializer, self).create(validated_data)
        user.set_password(plain_password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Method called when a user's data are updated, if the password is
        modified, hash the password before saving it in the database.
        """
        plain_password = validated_data.pop('password', None)
        user = super(UserPostSerializer, self).update(
            instance, validated_data
        )
        if plain_password:
            user.set_password(plain_password)
            user.save()
        return user

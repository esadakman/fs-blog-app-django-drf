from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from dj_rest_auth.serializers import TokenSerializer
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], 
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        ]

        extra_kwargs = { 
            "password": {"write_only": True},
            "password2": {"write_only": True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data.pop("password2")

        user = User.objects.create(**validated_data)
        user.password = make_password(password)
        user.save()
        return user

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return data


class UserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ('id', 'username','email', 'first_name', 'last_name')


class CustomTokenSerializer(TokenSerializer):

    user = UserTokenSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ('key', 'user')

class ProfileUpdateForm(serializers.ModelSerializer): 
    user = UserTokenSerializer()
    class Meta:
        model = Profile 
        fields = (
            'id',
            'image',
            'user'
        )

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.image = validated_data.get('image', instance.image)
        instance.save()

        user.username = user_data.get(
            'username',
            user.username
        )
        user.email = user_data.get(
            'email',
            user.email
         )
        user.first_name = user_data.get(
            'first_name',
            user.first_name
         )
        user.last_name = user_data.get(
            'last_name',
            user.last_name
         )
        user.id = user_data.get(
            'id',
            user.id
         ) 
        user.save()

        return instance
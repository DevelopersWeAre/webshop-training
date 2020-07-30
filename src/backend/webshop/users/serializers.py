from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import UserRBACRole

# Token manual

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class UserAccessManagementSerializer(serializers.ModelSerializer):
    """
    serializer for user role
    """

    class Meta:
        model = UserRBACRole
        fields = ("id", "role", "role_description")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for the current user
    """

    role = UserAccessManagementSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "online", "role")


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer for user detail
    """

    role = UserAccessManagementSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "avatar",
            "role",
        )


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    """
    serializer for user edit
    """

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password", "avatar", "role")

    def update(self, instance, validated_data):
        password = validated_data["password"]
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.role = validated_data.get("role", instance.role)
        instance.set_password(password)
        instance.save()
        return instance


class UserDetailUpdateSerializer2(serializers.ModelSerializer):
    """
    serializer for user edit
    """

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "avatar", "role")

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.role = validated_data.get("role", instance.role)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label="Email Adress")
    email2 = serializers.EmailField(label="Confirm Email")
    password = serializers.CharField(label="Password")
    password2 = serializers.CharField(label="Confirm Password")

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "email2",
            "password",
            "password2",
            "role",
            "avatar",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def validate(self, data):
        return data

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match!")
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This email is already registered.")
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get("password")
        password2 = value
        if password1 != password2:
            raise ValidationError("Passwords must match!")

    def create(self, validated_data):
        username = validated_data["username"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data["email"]
        password = validated_data["password"]
        role = validated_data["role"]
        avatar = validated_data["avatar"]
        user_obj = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            avatar=avatar,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "token", "is_superuser"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        user_a = User.objects.filter(username__iexact=username)
        user_b = User.objects.filter(email__iexact=username)
        user_qs = (user_a | user_b).distinct()
        if user_qs.exists() and user_qs.count() == 1:
            user_obj = user_qs.first()  # User.objects.get(id=1)
            password_passes = user_obj.check_password(password)
            if not user_obj.is_active:
                raise ValidationError("This user is inactive")
            # HTTPS
            if password_passes:
                # token
                data["username"] = user_obj.username
                # data["email"] = user_obj.email
                data["is_superuser"] = user_obj.is_superuser
                payload = jwt_payload_handler(user_obj)
                token = jwt_encode_handler(payload)
                data["token"] = token
                data["role"] = user_obj.role
                return data
        raise ValidationError("Unable to login with provided credentials!")

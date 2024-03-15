from django.core import exceptions
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        password2 = attrs.pop("password2")
        if attrs["password"] != password2:
            raise serializers.ValidationError(
                "Password and password confirmation do not match."
            )

        user = User(**attrs)
        errors = dict()
        try:
            # validate the password and catch the exception
            password_validation.validate_password(password=attrs["password"], user=user)
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"Error": "Email already exist"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class TodoSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Todo
        fields = "__all__"
        extra_kwargs = {"author": {"read_only": True}}
        read_only_fields =["author"]

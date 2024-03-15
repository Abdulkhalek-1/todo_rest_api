from django.shortcuts import get_object_or_404
from django.contrib.auth import logout, login, authenticate
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from . import serializers
from . import models


class TodoViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving todos.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: serializers.TodoSerializer(many=True)})
    def list(self, request):
        queryset = models.Todo.objects.filter(author=request.user)
        serializer = serializers.TodoSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=serializers.TodoSerializer(),
        responses={201: serializers.TodoSerializer()},
    )
    def create(self, request):
        serializer = serializers.TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={200: serializers.TodoSerializer()})
    def retrieve(self, request, pk=None):
        queryset = models.Todo.objects.filter(author=request.user)
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.TodoSerializer(user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = models.Todo.objects.filter(author=request.user)
        todo = get_object_or_404(queryset, pk=pk)
        todo.delete()
        return Response(status=204)

    @swagger_auto_schema(
        request_body=serializers.TodoSerializer(),
        responses={201: serializers.TodoSerializer()},
    )
    def update(self, request, pk=None):
        queryset = models.Todo.objects.filter(author=request.user)
        todo = get_object_or_404(queryset, pk=pk)
        serializer = serializers.TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        request_body=serializers.TodoSerializer(),
        responses={201: serializers.TodoSerializer()},
    )
    def partial_update(self, request, pk=None):
        queryset = models.Todo.objects.filter(author=request.user)
        todo = get_object_or_404(queryset, pk=pk)
        serializer = serializers.TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserLoginView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(serializers.UserSerializer(user).data)
        else:
            return Response({"error": "Invalid credentials"}, status=400)


class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"success": "Logged out successfully"})


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # type: ignore
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

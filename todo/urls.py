from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"todos", views.TodoViewSet, basename="todos")

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
    path("register/", views.UserRegistrationAPIView.as_view(), name="user_register"),
]

urlpatterns += router.urls

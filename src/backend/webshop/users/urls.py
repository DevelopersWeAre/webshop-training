from django.urls import path

from .views import (
    UserListAPIView,
    UserLoginAPIView,
    UserDetailAPIView,
    UserLogoutAPIView,
    RBAC_role_list,
    RBAC_role_detail,
    UserUpdateAPIView,
    UsersExport,
)

urlpatterns = [
    path("list/", UserListAPIView.as_view(), name="user_list"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("create/", UserListAPIView.as_view(), name="user_create"),
    path("<int:pk>/", UserDetailAPIView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("logout/", UserLogoutAPIView.as_view(), name="user_logout"),
    path("role/list/", RBAC_role_list, name="role_list"),
    path("role/<int:role_pk>/", RBAC_role_detail, name="role_detail"),
]
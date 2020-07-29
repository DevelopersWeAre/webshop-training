from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Message, Company, UserRBACRole
from users.serializers import (
    UserLoginSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserAccessManagementSerializer,
    UserDetailSerializer,
    UserDetailUpdateSerializer,
    UserDetailUpdateSerializer2,
)

User = get_user_model()
permission_handler = PermissionHandler()


class UserListAPIView(APIView):
    def get(self, request, format=None):
        """
        Lists all users or users by company if user is not superadmin
        :param request:
        :param format:
        :return:
        """

        if request.user.is_superuser:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif (
            request.user.role.role in ("COMPANY_ADMINISTRATOR", "TEST_MANAGER")
            and request.user.is_active
        ):
            users_by_company = User.objects.filter(company=request.user.company)
            serializer = UserSerializer(users_by_company, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "User has no permission to access this list."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def post(self, request):
        """
        Used to create user
        :param request:
        :return:
        """

        serializer = UserCreateSerializer(data=request.data)
        company = Company.objects.get(pk=request.user.company.id)

        if request.user.is_superuser:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif (
            request.user.role.role in ("COMPANY_ADMINISTRATOR", "TEST_MANAGER")
            and request.user.is_active
        ):
            if serializer.is_valid():
                serializer.save(company=company)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Error creating user"})


class UserDetailAPIView(APIView):
    """
    Single user operations
    """

    def get_object(self, pk: int):
        """
        Retrive user object
        :param pk:
        :return:
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist as ex:
            logger.exception("Error ocurred {}".format(ex.args))
            return Response(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk: int, format=None):
        """
        Single user detail
        :param request:
        :param pk:
        :param format:
        :return:
        """

        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk: int, format=None):
        """
        Update single user
        :param request:
        :param pk:
        :param format:
        :return:
        """

        user = self.get_object(pk)
        serializer = UserDetailUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int, format=None):
        """
        Deletes single user
        :param request:
        :param pk:
        :param format:
        :return:
        """

        user = self.get_object(pk)
        user.delete()
        return Response(
            {"message": "User has been deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserUpdateAPIView(APIView):
    def get_object(self, pk: int):
        """
        Retrive user object
        :param pk:
        :return:
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist as ex:
            logger.exception("Error ocurred {}".format(ex.args))
            return Response(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk: int, format=None):
        """
        Update single user
        :param request:
        :param pk:
        :param format:
        :return:
        """

        user = self.get_object(pk)
        serializer = UserDetailUpdateSerializer2(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not request.user.is_anonymous:
            request.user.delete_token()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes((IsAuthenticated,))
def RBAC_role_list(request):
    """
    RBAC role endpoint
    :param request:
    :return:
    """
    if request.method == "GET":
        roles = UserRBACRole.objects.all()
        serializer = UserAccessManagementSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = UserAccessManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            log(
                user=request.user,
                action="CREATED_NEW_ROLE: {}".format(serializer.data["role"]),
                obj=UserRBACRole.objects.get(pk=serializer.data["id"]),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "ERROR occurred: {}".format(serializer.errors)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticated,))
def RBAC_role_detail(request, role_pk: int):
    """
    RBAC role detail
    :param request:
    :param role_pk:
    :return:
    """

    try:
        rbac_role = UserRBACRole.objects.get(pk=role_pk)
    except UserRBACRole.DoesNotExist as ex:
        logger.exception("ERROR: {}".format(ex.args))
        return Response(
            {"message": "Requested role doesn't exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = UserAccessManagementSerializer(rbac_role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = UserAccessManagementSerializer(rbac_role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            log(
                user=request.user,
                action="UDPATED_ROLE: {}".format(rbac_role.role),
                obj=rbac_role,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.exception("ERROR {}".format(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        rbac_role.delete()
        log(
            user=request.user,
            action="DELETED_ROLE:{}".format(rbac_role.role),
            obj=rbac_role,
        )
        return Response(
            {"message": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT
        )
    else:
        return Response(
            {"message": "Incorrect request"}, status=status.HTTP_400_BAD_REQUEST
        )



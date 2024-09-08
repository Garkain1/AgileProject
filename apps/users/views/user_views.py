from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from ..models import User
from ..serializers import UserListSerializer, RegisterUserSerializer


class UserListGenericView(ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        project_name = self.request.query_params.get('project_name')

        if project_name:
            return User.objects.filter(project__name=project_name)

        return User.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        users = self.get_queryset()

        if not users.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUserGenericView(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

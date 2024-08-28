from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from ..models import Tag
from ..serializers import TagSerializer


class TagListAPIView(APIView):

    def get_objects(self) -> Tag:
        return Tag.objects.all()

    def get(self, request: Request) -> Response:
        tags = self.get_objects()
        if not tags.exists():
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


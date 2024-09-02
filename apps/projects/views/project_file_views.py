from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import get_object_or_404
from ..models import ProjectFile, Project
from ..serializers import AllProjectFilesSerializer, CreateProjectFileSerializer, ProjectFileDetailSerializer
from ..utils import delete_file


class ProjectFileListGenericView(ListCreateAPIView):
    serializer_class = CreateProjectFileSerializer

    def get_queryset(self):
        project_name = self.request.query_params.get('project')
        if project_name:
            return ProjectFile.objects.filter(project__name=project_name)
        return ProjectFile.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        project_files = self.get_queryset()
        if not project_files.exists():
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)

        serializer = AllProjectFilesSerializer(project_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs) -> Response:
        file_content = request.FILES["file"]
        project_id = request.data["project_id"]
        request.data['file_name'] = file_content.name if file_content else None

        project = get_object_or_404(Project, pk=project_id)

        serializer = self.get_serializer(
            data=request.data,
            context={
                "raw_file": file_content,
                "project": project
            }
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectFileDetailGenericView(RetrieveDestroyAPIView):
    serializer_class = ProjectFileDetailSerializer

    def get_object(self):
        return get_object_or_404(ProjectFile, pk=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        project_file = self.get_object()
        serializer = self.get_serializer(project_file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        project_file = self.get_object()
        try:
            delete_file(file_path=project_file.file_path.path)
            project_file.delete()
            return Response({"message": "File deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
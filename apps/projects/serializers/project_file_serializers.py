from rest_framework import serializers
from ..models import ProjectFile
from ..utils import check_extension, create_file_path, check_file_size, save_file


class AllProjectFilesSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = ProjectFile
        fields = ('id', 'file_name', 'projects')

    def get_projects(self, obj):
        return [project.name for project in obj.projects.all()]


class CreateProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ('file_name',)

    def validate_file_name(self, value: str) -> str:
        if not value.isascii():
            raise serializers.ValidationError("Please, provide a valid file name.")
        if not check_extension(value):
            raise serializers.ValidationError("Valid file extensions: ['.csv', '.doc', '.pdf', '.xlsx']")
        return value

    def create(self, validated_data):
        project = self.context.get('project')
        raw_file = self.context.get('raw_file')
        file_path = create_file_path(project_name=project.name, file_name=validated_data['file_name'])

        if check_file_size(file=raw_file):
            save_file(file_path=file_path, file_content=raw_file)
            validated_data['file_path'] = file_path
            return ProjectFile.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("File size is too large (2 MB as maximum).")


class ProjectFileDetailSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = ProjectFile
        fields = ('id', 'file_name', 'created_at', 'projects')

    def get_projects(self, obj):
        return [project.name for project in obj.projects.all()]

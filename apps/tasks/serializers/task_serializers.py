from typing import Any
from rest_framework import serializers
from django.utils import timezone
from ..models import Task, Tag
from ..choices import Priority
from ..dependencies import Project, ProjectShortInfoSerializer


class AllTasksSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(read_only=True, slug_field='name')
    assignee = serializers.SlugRelatedField(read_only=True, slug_field='email')
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Task
        fields = ('id', 'name', 'status', 'priority', 'project', 'assignee', 'deadline')


class CreateUpdateTaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field='name', queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = ('name', 'description', 'priority', 'project', 'tags', 'status', 'deadline')

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags:
            instance.tags.set(tags)
        instance.save()
        return instance

    def validate_name(self, value: str) -> str:
        if len(value) < 10:
            raise serializers.ValidationError("The name of the task couldn't be less than 10 characters")
        return value

    def validate_description(self, value: str) -> str:
        if len(value) < 50:
            raise serializers.ValidationError("The description of the task couldn't be less than 50 characters")
        return value

    def validate_priority(self, value: int) -> int:
        if value not in [val[0] for val in Priority.choices()]:
            raise serializers.ValidationError("The priority of the task couldn't be one of the available options")
        return value

    def validate_project(self, value: str) -> str:
        if not Project.objects.filter(name=value).exists():
            raise serializers.ValidationError("The project with this name couldn't be found in the database")
        return value

    def validate_tags(self, value: list[str, ...]) -> list[str, ...]:
        if not Tag.objects.filter(name__in=value).exists():
            raise serializers.ValidationError("The tags couldn't be found in the database")
        return value

    def validate_deadline(self, value):
        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.get_current_timezone())
        if value < timezone.now():
            raise serializers.ValidationError("The deadline cannot be in the past.")
        return value

    def create(self, validated_data: dict[str, Any]) -> Task:
        tags = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        for tag in tags:
            task.tags.add(tag)
        task.save()
        return task


class TaskDetailSerializer(serializers.ModelSerializer):
    project = ProjectShortInfoSerializer()
    tags = serializers.StringRelatedField(many=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Task
        exclude = ('updated_at', 'deleted_at')

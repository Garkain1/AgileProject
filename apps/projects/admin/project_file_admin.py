from django.contrib import admin
from ..models.project_file import ProjectFile


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_path', 'created_at']
    search_fields = ['file_name']
    list_filter = ['created_at']

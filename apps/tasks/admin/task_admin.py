from django.contrib import admin
from ..models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'status', 'priority', 'created_at', 'deadline']
    search_fields = ['name']
    list_filter = ['status', 'priority', 'project', 'created_at', 'deadline']
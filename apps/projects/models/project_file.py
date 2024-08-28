from django.db import models
from ..utils import get_project_file_path


class ProjectFile(models.Model):
    file_name = models.CharField(max_length=120)
    file_path = models.FileField(upload_to=get_project_file_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-created_at']

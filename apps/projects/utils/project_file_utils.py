from django.conf import settings
import os


def get_project_file_path(instance, filename):
    return os.path.join(settings.PROJECTS_FILES_PATH, filename)

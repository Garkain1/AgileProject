import os
from pathlib import Path
from django.conf import settings

ALLOWED_EXTENSIONS = ['.csv', '.doc', '.pdf', '.xlsx']


def check_extension(filename):
    extension = Path(filename).suffix
    if extension not in ALLOWED_EXTENSIONS:
        return False
    return True


def check_file_size(file, required_size=2):
    file_size = file.size / (1024 * 1024)
    if file_size > required_size:
        return False
    return True


def create_file_path(project_name, file_name):
    new_file_name, file_ext = file_name.split('.')
    sanitized_project_name = project_name.replace(' ', '_')
    sanitized_file_name = new_file_name.replace(' ', '_')
    file_path = os.path.join(settings.MEDIA_ROOT, settings.PROJECTS_FILES_PATH, sanitized_project_name,
                             f"{sanitized_file_name}.{file_ext}")
    return file_path


def save_file(file_path, file_content):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        for chunk in file_content.chunks():
            f.write(chunk)
    return file_path


def delete_file(file_path):
    os.remove(os.path.realpath(file_path))

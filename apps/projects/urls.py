from django.urls import path
from .views import (ProjectsListAPIView, ProjectDetailAPIView, ProjectFileListGenericView, ProjectFileDetailGenericView,
                    DownloadProjectFileView)

urlpatterns = [
    path('', ProjectsListAPIView.as_view(), name='project-list-create'),
    path('<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('files/', ProjectFileListGenericView.as_view()),
    path('files/download/<int:pk>/', DownloadProjectFileView.as_view(), name='download_file'),
    path('files/<int:pk>/', ProjectFileDetailGenericView.as_view(), name='file-detail'),
]

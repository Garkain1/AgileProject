from django.urls import path
from .views import ProjectsListAPIView, ProjectDetailAPIView, ProjectFileListAPIView

urlpatterns = [
    path('', ProjectsListAPIView.as_view(), name='project-list-create'),
    path('<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('files/', ProjectFileListAPIView.as_view()),
]

from django.urls import path
from .views import TagListAPIView, TagDetailAPIView, TasksListAPIView

urlpatterns = [
    path('tags/', TagListAPIView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagDetailAPIView.as_view()),
    path('', TasksListAPIView.as_view(), name='tasks-list-create'),
]

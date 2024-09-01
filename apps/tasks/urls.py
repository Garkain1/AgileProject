from django.urls import path
from .views import TagListAPIView, TagDetailAPIView

urlpatterns = [
    path('tags/', TagListAPIView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagDetailAPIView.as_view()),
]

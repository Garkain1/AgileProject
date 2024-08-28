from django.urls import path
from .views import TagListAPIView

urlpatterns = [
    path('tags/', TagListAPIView.as_view(), name='tag-list-create'),
]

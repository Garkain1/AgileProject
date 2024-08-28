from django.urls import include, path

urlpatterns = [
    path('tasks/', include('apps.tasks.urls')),
]
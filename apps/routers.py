from django.urls import include, path

urlpatterns = [
    path('tasks/', include('apps.tasks.urls')),
    path('projects/', include('apps.projects.urls')),
    path('users/', include('apps.users.urls')),
]

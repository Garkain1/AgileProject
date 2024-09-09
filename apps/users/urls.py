from django.urls import path
from apps.users.views import UserListGenericView, RegisterUserGenericView, UserDetailView

urlpatterns = [
    path('', UserListGenericView.as_view(), name='user-list'),
    path('register/', RegisterUserGenericView.as_view(), name='user-register'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]

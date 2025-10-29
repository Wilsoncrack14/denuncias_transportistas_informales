from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,

    MyProfileView,
    UpdateMyProfileView,
    ChangePasswordView
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    
    path('profile/', MyProfileView.as_view(), name='my-profile'),
    path('profile/update/', UpdateMyProfileView.as_view(), name='update-my-profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
]

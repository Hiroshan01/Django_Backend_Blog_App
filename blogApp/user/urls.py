from django.urls import path
from . import views
from knox import views as knox_views

urlpatterns = [
    path('api/register/', views.register_api, name='register'),
    path('api/login/', views.login_api, name='login'),
    path('api/user/', views.get_user_data, name='user'),
    path('api/logout/', knox_views.LogoutView.as_view()),
    path('api/logoutAll/', knox_views.LogoutAllView.as_view()),

    path('api/posts/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', views.PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
]


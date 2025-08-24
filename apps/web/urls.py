from django.urls import path
from . import views, admin_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin User Management URLs
    path('admin/users/', admin_views.user_management, name='user_management'),
    path('admin/users/create/', admin_views.create_user, name='create_user'),
    path('admin/users/create-admin/', admin_views.create_admin_account, name='create_admin_account'),
    path('admin/users/<int:user_id>/edit/', admin_views.edit_user, name='edit_user'),
    path('admin/users/<int:user_id>/details/', admin_views.user_details, name='user_details'),
    path('admin/users/<int:user_id>/reset-password/', admin_views.reset_user_password, name='reset_user_password'),
    path('admin/api/toggle-user-status/', admin_views.toggle_user_status, name='toggle_user_status'),
    path('admin/api/delete-user/', admin_views.delete_user, name='delete_user'),
]

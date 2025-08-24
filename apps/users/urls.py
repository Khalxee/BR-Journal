from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
]

from django.urls import path
from . import views

urlpatterns = [
    # Document management
    path('', views.document_list, name='document_list'),
    path('create/', views.create_document, name='create_document'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('<int:pk>/edit/', views.edit_document, name='edit_document'),
    path('<int:pk>/delete/', views.delete_document, name='delete_document'),
    path('<int:pk>/export/', views.export_document, name='export_document'),
    path('<int:pk>/email/', views.email_document, name='email_document'),
    
    # Settings management
    path('settings/', views.settings_dashboard, name='settings_dashboard'),
    path('settings/templates/', views.manage_templates, name='manage_templates'),
    path('settings/letterheads/', views.manage_letterheads, name='manage_letterheads'),
    path('settings/document-types/', views.manage_document_types, name='manage_document_types'),
    path('settings/signatories/', views.manage_signatories, name='manage_signatories'),
    path('settings/qrcodes/', views.manage_qrcodes, name='manage_qrcodes'),
    
    # History
    path('history/', views.document_history, name='document_history'),
    
    # User management (admin only)
    path('users/', views.user_management, name='user_management'),
]

from django.urls import path
from . import views
from . import views_topman
from . import views_summary

app_name = 'journal'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Journal CRUD
    path('list/', views.JournalListView.as_view(), name='list'),
    path('create/', views.JournalCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', views.JournalDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.JournalUpdateView.as_view(), name='update'),
    
    # Comments
    path('comment/<int:journal_id>/', views.add_comment, name='add_comment'),
    
    # Summary Report
    path('summary/', views_summary.SummaryReportView.as_view(), name='summary_report'),
    path('summary/export/', views_summary.export_summary_report, name='export_summary'),
    
    # Top Management Features (Admin Only)
    path('topman/', views_topman.TopManagementReportListView.as_view(), name='topman_report_list'),
    path('topman/create/', views_topman.TopManagementReportCreateView.as_view(), name='topman_report_create'),
    path('topman/detail/<int:pk>/', views_topman.TopManagementReportDetailView.as_view(), name='topman_report_detail'),
    path('topman/update/<int:pk>/', views_topman.TopManagementReportUpdateView.as_view(), name='topman_report_update'),
    path('topman/tagging/', views_topman.topman_tagging_interface, name='topman_tagging'),
    path('topman/summary/', views_topman.topman_weekly_summary, name='topman_summary'),
    
    # AJAX endpoints for tagging
    path('ajax/tag-item/', views_topman.ajax_tag_item, name='ajax_tag_item'),
]

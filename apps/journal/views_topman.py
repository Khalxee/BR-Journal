from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime, timedelta, date
from .models import WeeklyJournal, TopManagementReport, TopManagementTag
from .forms_topman import TopManagementReportForm, TopManagementTagForm, WeekSelectionForm
import json


def is_admin_user(user):
    """Check if user is admin (staff or superuser)"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin privileges"""
    
    def test_func(self):
        return is_admin_user(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, "You need administrator privileges to access this page.")
        return redirect('journal:dashboard')


# Top Management Report Views
class TopManagementReportListView(AdminRequiredMixin, ListView):
    """List all top management reports - Admin only"""
    model = TopManagementReport
    template_name = 'journal/topman/report_list.html'
    context_object_name = 'reports'
    paginate_by = 10
    
    def get_queryset(self):
        return TopManagementReport.objects.select_related('created_by').prefetch_related('tagged_items')


class TopManagementReportDetailView(AdminRequiredMixin, DetailView):
    """View top management report details - Admin only"""
    model = TopManagementReport
    template_name = 'journal/topman/report_detail.html'
    context_object_name = 'report'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.object
        
        # Get tagged items organized by department
        context['tagged_items_by_department'] = report.get_tagged_items_by_department()
        
        # Get all tagged items with priority ordering
        context['all_tagged_items'] = report.get_all_tagged_items()
        
        # Priority statistics
        context['priority_stats'] = {
            'high': report.tagged_items.filter(priority='high').count(),
            'medium': report.tagged_items.filter(priority='medium').count(),
            'low': report.tagged_items.filter(priority='low').count(),
        }
        
        return context


class TopManagementReportCreateView(AdminRequiredMixin, CreateView):
    """Create new top management report - Admin only"""
    model = TopManagementReport
    form_class = TopManagementReportForm
    template_name = 'journal/topman/report_form.html'
    success_url = reverse_lazy('journal:topman_report_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Top Management report created successfully!")
        return super().form_valid(form)


class TopManagementReportUpdateView(AdminRequiredMixin, UpdateView):
    """Edit top management report - Admin only"""
    model = TopManagementReport
    form_class = TopManagementReportForm
    template_name = 'journal/topman/report_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Top Management report updated successfully!")
        return super().form_valid(form)


@staff_member_required
def topman_tagging_interface(request):
    """Interface for admins to tag journal items for top management"""
    week_form = WeekSelectionForm(request.GET or None)
    
    # Get week range from form or use current week
    if week_form.is_valid():
        week_start = week_form.cleaned_data['week_start']
        week_end = week_form.cleaned_data['week_end']
    else:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
    
    # Get or create top management report for this week
    report, created = TopManagementReport.objects.get_or_create(
        week_start=week_start,
        week_end=week_end,
        defaults={
            'created_by': request.user,
            'title': f"Top Management Report - {week_start.strftime('%B %d')} to {week_end.strftime('%B %d, %Y')}"
        }
    )
    
    # Get all journal entries for this week
    journal_entries = WeeklyJournal.objects.filter(
        date_from__lte=week_end,
        date_to__gte=week_start
    ).select_related('author', 'department').order_by('department__name', 'author__last_name')
    
    # Get already tagged items for this report
    existing_tags = TopManagementTag.objects.filter(report=report).values_list(
        'journal_entry_id', 'section', 'item_index'
    )
    
    # Create a set for quick lookup of tagged items
    tagged_items = set()
    for tag in existing_tags:
        tagged_items.add((tag[0], tag[1], tag[2]))
    
    context = {
        'week_form': week_form,
        'week_start': week_start,
        'week_end': week_end,
        'report': report,
        'journal_entries': journal_entries,
        'tagged_items': tagged_items,
        'created_report': created
    }
    
    return render(request, 'journal/topman/tagging_interface.html', context)


@staff_member_required
def ajax_tag_item(request):
    """AJAX endpoint to tag/untag journal items for top management"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST method required'})
    
    try:
        journal_id = request.POST.get('journal_id')
        section = request.POST.get('section')
        item_index = int(request.POST.get('item_index'))
        action = request.POST.get('action')  # 'tag' or 'untag'
        report_id = request.POST.get('report_id')
        priority = request.POST.get('priority', 'medium')
        admin_note = request.POST.get('admin_note', '')
        
        journal_entry = get_object_or_404(WeeklyJournal, id=journal_id)
        report = get_object_or_404(TopManagementReport, id=report_id)
        
        if action == 'tag':
            # Get the item data based on section
            items = getattr(journal_entry, f'get_{section}_list')()
            if item_index < len(items):
                item = items[item_index]
                
                # Create or update tag
                tag, created = TopManagementTag.objects.get_or_create(
                    journal_entry=journal_entry,
                    section=section,
                    item_index=item_index,
                    report=report,
                    defaults={
                        'item_text': item.get('text', ''),
                        'item_status': item.get('status', 'not_started'),
                        'tagged_by': request.user,
                        'priority': priority,
                        'admin_note': admin_note
                    }
                )
                
                if not created:
                    # Update existing tag
                    tag.priority = priority
                    tag.admin_note = admin_note
                    tag.save()
                
                return JsonResponse({
                    'success': True,
                    'action': 'tagged',
                    'created': created
                })
        
        elif action == 'untag':
            # Remove tag
            TopManagementTag.objects.filter(
                journal_entry=journal_entry,
                section=section,
                item_index=item_index,
                report=report
            ).delete()
            
            return JsonResponse({
                'success': True,
                'action': 'untagged'
            })
        
        return JsonResponse({'success': False, 'error': 'Invalid action'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
def topman_weekly_summary(request):
    """Generate weekly summary view for top management"""
    week_form = WeekSelectionForm(request.GET or None)
    
    # Get week range from form or use current week
    if week_form.is_valid():
        week_start = week_form.cleaned_data['week_start']
        week_end = week_form.cleaned_data['week_end']
    else:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
    
    # Get journal entries for this week
    journal_entries = WeeklyJournal.objects.filter(
        date_from__lte=week_end,
        date_to__gte=week_start
    ).select_related('author', 'department')
    
    # Get existing report for this week
    try:
        report = TopManagementReport.objects.get(week_start=week_start, week_end=week_end)
        tagged_items = report.get_all_tagged_items()
    except TopManagementReport.DoesNotExist:
        report = None
        tagged_items = []
    
    # Calculate statistics
    stats = {
        'total_entries': journal_entries.count(),
        'total_departments': journal_entries.values('department').distinct().count(),
        'total_team_members': journal_entries.values('author').distinct().count(),
        'tagged_items_count': len(tagged_items),
    }
    
    # Status summary across all entries
    status_summary = {
        'completed': 0,
        'in_progress': 0,
        'on_hold': 0,
        'not_started': 0,
        'cancelled': 0
    }
    
    for entry in journal_entries:
        all_items = []
        all_items.extend(entry.get_highlights_list())
        all_items.extend(entry.get_pendings_list())
        all_items.extend(entry.get_challenges_list())
        all_items.extend(entry.get_personal_updates_list())
        all_items.extend(entry.get_strategies_list())
        
        for item in all_items:
            status = item.get('status', 'not_started')
            if status in status_summary:
                status_summary[status] += 1
    
    context = {
        'week_form': week_form,
        'week_start': week_start,
        'week_end': week_end,
        'journal_entries': journal_entries,
        'report': report,
        'tagged_items': tagged_items,
        'stats': stats,
        'status_summary': status_summary,
    }
    
    return render(request, 'journal/topman/weekly_summary.html', context)

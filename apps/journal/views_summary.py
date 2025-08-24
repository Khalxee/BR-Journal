from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Prefetch
from django.template.loader import render_to_string
from datetime import datetime, timedelta, date
from .models import WeeklyJournal, Department, JournalComment
from .forms import WeeklyJournalForm, JournalCommentForm
import json


class SummaryReportView(LoginRequiredMixin, ListView):
    """Consolidated summary report of all journal entries with date filtering"""
    model = WeeklyJournal
    template_name = 'journal/summary_report.html'
    context_object_name = 'journal_entries'
    
    def get_queryset(self):
        queryset = WeeklyJournal.objects.select_related('author', 'department').prefetch_related('comments')
        
        # Date filtering
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(date_from__gte=date_from_obj)
            except ValueError:
                pass
                
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(date_to__lte=date_to_obj)
            except ValueError:
                pass
        
        # Default to current month if no dates specified
        if not date_from and not date_to:
            today = date.today()
            first_of_month = today.replace(day=1)
            queryset = queryset.filter(date_from__gte=first_of_month)
        
        # Department filtering
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        
        # Author filtering
        author_id = self.request.GET.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(highlights__icontains=search) |
                Q(pendings__icontains=search) |
                Q(challenges__icontains=search) |
                Q(personal_updates__icontains=search) |
                Q(strategies__icontains=search)
            )
        
        # Group by option
        group_by = self.request.GET.get('group_by', 'date')
        if group_by == 'department':
            queryset = queryset.order_by('department__name', '-date_from', 'author__last_name')
        elif group_by == 'author':
            queryset = queryset.order_by('author__last_name', 'author__first_name', '-date_from')
        else:  # Default to date
            queryset = queryset.order_by('-date_from', 'department__name', 'author__last_name')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter parameters for form population
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        context['selected_department'] = self.request.GET.get('department', '')
        context['selected_author'] = self.request.GET.get('author', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['group_by'] = self.request.GET.get('group_by', 'date')
        
        # Get all departments and authors for filter dropdowns
        context['departments'] = Department.objects.all().order_by('name')
        context['authors'] = WeeklyJournal.objects.select_related('author').values(
            'author__id', 'author__first_name', 'author__last_name', 'author__username'
        ).distinct().order_by('author__last_name', 'author__first_name')
        
        # Calculate summary statistics
        entries = context['journal_entries']
        
        # Overall statistics
        context['stats'] = {
            'total_entries': entries.count(),
            'departments_count': entries.values('department').distinct().count(),
            'authors_count': entries.values('author').distinct().count(),
            'date_range': self.get_date_range_display(),
        }
        
        # Status summary across all entries
        status_summary = {
            'completed': 0,
            'in_progress': 0,
            'on_hold': 0,
            'not_started': 0,
            'cancelled': 0,
            'total_items': 0
        }
        
        for entry in entries:
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
                status_summary['total_items'] += 1
        
        context['status_summary'] = status_summary
        
        # Group entries for display
        context['grouped_entries'] = self.group_entries(entries, context['group_by'])
        
        return context
    
    def get_date_range_display(self):
        """Get human-readable date range for display"""
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if date_from and date_to:
            try:
                from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                return f"{from_obj.strftime('%b %d, %Y')} - {to_obj.strftime('%b %d, %Y')}"
            except ValueError:
                pass
        elif date_from:
            try:
                from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                return f"From {from_obj.strftime('%b %d, %Y')}"
            except ValueError:
                pass
        elif date_to:
            try:
                to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                return f"Until {to_obj.strftime('%b %d, %Y')}"
            except ValueError:
                pass
        else:
            # Default current month
            today = date.today()
            return f"{today.strftime('%B %Y')} (Current Month)"
    
    def group_entries(self, entries, group_by):
        """Group entries based on the selected grouping option"""
        if group_by == 'department':
            grouped = {}
            for entry in entries:
                dept_name = entry.department.name
                if dept_name not in grouped:
                    grouped[dept_name] = []
                grouped[dept_name].append(entry)
            return grouped
        elif group_by == 'author':
            grouped = {}
            for entry in entries:
                author_name = entry.author.get_full_name() or entry.author.username
                if author_name not in grouped:
                    grouped[author_name] = []
                grouped[author_name].append(entry)
            return grouped
        else:  # date grouping
            grouped = {}
            for entry in entries:
                date_key = f"{entry.date_from.strftime('%B %d')} - {entry.date_to.strftime('%B %d, %Y')}"
                if date_key not in grouped:
                    grouped[date_key] = []
                grouped[date_key].append(entry)
            return grouped


@login_required
def export_summary_report(request):
    """Export summary report as CSV or print-friendly HTML"""
    export_format = request.GET.get('format', 'html')
    
    # Get the same queryset as the summary report
    summary_view = SummaryReportView()
    summary_view.request = request
    queryset = summary_view.get_queryset()
    
    if export_format == 'csv':
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="journal_summary_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Date From', 'Date To', 'Author', 'Department', 
            'Highlights', 'Pendings', 'Challenges', 'Personal Updates', 'Strategies'
        ])
        
        for entry in queryset:
            # Convert JSON lists to readable strings
            highlights = ' | '.join([item.get('text', '') for item in entry.get_highlights_list()])
            pendings = ' | '.join([item.get('text', '') for item in entry.get_pendings_list()])
            challenges = ' | '.join([item.get('text', '') for item in entry.get_challenges_list()])
            personal = ' | '.join([item.get('text', '') for item in entry.get_personal_updates_list()])
            strategies = ' | '.join([item.get('text', '') for item in entry.get_strategies_list()])
            
            writer.writerow([
                entry.date_from.strftime('%Y-%m-%d'),
                entry.date_to.strftime('%Y-%m-%d'),
                entry.author.get_full_name() or entry.author.username,
                entry.department.name,
                highlights[:500] + '...' if len(highlights) > 500 else highlights,
                pendings[:500] + '...' if len(pendings) > 500 else pendings,
                challenges[:500] + '...' if len(challenges) > 500 else challenges,
                personal[:500] + '...' if len(personal) > 500 else personal,
                strategies[:500] + '...' if len(strategies) > 500 else strategies,
            ])
        
        return response
    
    else:  # HTML print format
        # Create a new instance of the view and set the request
        summary_view = SummaryReportView()
        summary_view.request = request
        summary_view.kwargs = {}
        
        # Get the queryset and context data
        queryset = summary_view.get_queryset()
        summary_view.object_list = queryset
        
        # Get proper context data
        try:
            context = summary_view.get_context_data()
        except Exception as e:
            # Fallback context if get_context_data fails
            context = {
                'journal_entries': queryset,
                'stats': {
                    'total_entries': queryset.count(),
                    'departments_count': queryset.values('department').distinct().count(),
                    'authors_count': queryset.values('author').distinct().count(),
                    'date_range': summary_view.get_date_range_display(),
                }
            }
        
        context['print_mode'] = True
        context['export_date'] = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        # Ensure all context variables are available
        if 'group_by' not in context:
            context['group_by'] = request.GET.get('group_by', 'date')
        if 'grouped_entries' not in context:
            context['grouped_entries'] = summary_view.group_entries(queryset, context['group_by'])
        
        # Ensure status summary is available
        if 'status_summary' not in context:
            status_summary = {
                'completed': 0, 'in_progress': 0, 'on_hold': 0, 
                'not_started': 0, 'cancelled': 0, 'total_items': 0
            }
            for entry in queryset:
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
                    status_summary['total_items'] += 1
            
            context['status_summary'] = status_summary
        
        return render(request, 'journal/summary_report_print.html', context)

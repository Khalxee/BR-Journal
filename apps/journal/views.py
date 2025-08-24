from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from .models import WeeklyJournal, Department, JournalComment
from .forms import WeeklyJournalForm, JournalCommentForm


class JournalListView(LoginRequiredMixin, ListView):
    """View to list all journal entries"""
    model = WeeklyJournal
    template_name = 'journal/journal_list.html'
    context_object_name = 'journals'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = WeeklyJournal.objects.select_related('author', 'department')
        
        # Filter by department if specified
        dept_id = self.request.GET.get('department')
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
            
        # Filter by date range if specified
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(date_from__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_to__lte=date_to)
            
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(highlights__icontains=search) |
                Q(challenges__icontains=search) |
                Q(strategies__icontains=search) |
                Q(author__first_name__icontains=search) |
                Q(author__last_name__icontains=search) |
                Q(department__name__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['current_filters'] = {
            'department': self.request.GET.get('department', ''),
            'date_from': self.request.GET.get('date_from', ''),
            'date_to': self.request.GET.get('date_to', ''),
            'search': self.request.GET.get('search', ''),
        }
        return context


class JournalDetailView(LoginRequiredMixin, DetailView):
    """View to display a single journal entry"""
    model = WeeklyJournal
    template_name = 'journal/journal_detail.html'
    context_object_name = 'journal'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author')
        context['comment_form'] = JournalCommentForm()
        return context



class JournalCreateView(LoginRequiredMixin, CreateView):
    """View to create a new journal entry"""
    model = WeeklyJournal
    form_class = WeeklyJournalForm
    template_name = 'journal/journal_form.html'
    success_url = reverse_lazy('journal:list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Journal entry created successfully!')
        return super().form_valid(form)


class JournalUpdateView(LoginRequiredMixin, UpdateView):
    """View to update an existing journal entry"""
    model = WeeklyJournal
    form_class = WeeklyJournalForm
    template_name = 'journal/journal_form.html'
    
    def get_queryset(self):
        # Users can only edit their own journal entries
        return WeeklyJournal.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Journal entry updated successfully!')
        return super().form_valid(form)


@login_required
def add_comment(request, journal_id):
    """AJAX view to add a comment to a journal entry"""
    if request.method == 'POST':
        journal = get_object_or_404(WeeklyJournal, id=journal_id)
        form = JournalCommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.journal = journal
            comment.author = request.user
            comment.save()
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.get_full_name() or comment.author.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def dashboard(request):
    """Dashboard view showing journal statistics and recent entries"""
    user_journals = WeeklyJournal.objects.filter(author=request.user).order_by('-date_from')[:5]
    recent_journals = WeeklyJournal.objects.select_related('author', 'department').order_by('-created_at')[:10]
    
    # Get current week dates for quick entry
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Calculate status summary across all entries
    all_journals = WeeklyJournal.objects.all()
    status_summary = {
        'completed': 0,
        'in_progress': 0,
        'on_hold': 0,
        'not_started': 0,
        'cancelled': 0,
        'total_items': 0
    }
    
    for journal in all_journals:
        all_items = []
        all_items.extend(journal.get_highlights_list())
        all_items.extend(journal.get_pendings_list())
        all_items.extend(journal.get_challenges_list())
        all_items.extend(journal.get_personal_updates_list())
        all_items.extend(journal.get_strategies_list())
        
        for item in all_items:
            status = item.get('status', 'not_started')
            if status in status_summary:
                status_summary[status] += 1
            status_summary['total_items'] += 1
    
    # User-specific status summary
    user_status_summary = {
        'completed': 0,
        'in_progress': 0,
        'on_hold': 0,
        'not_started': 0,
        'cancelled': 0,
        'total_items': 0
    }
    
    user_all_journals = WeeklyJournal.objects.filter(author=request.user)
    for journal in user_all_journals:
        all_items = []
        all_items.extend(journal.get_highlights_list())
        all_items.extend(journal.get_pendings_list())
        all_items.extend(journal.get_challenges_list())
        all_items.extend(journal.get_personal_updates_list())
        all_items.extend(journal.get_strategies_list())
        
        for item in all_items:
            status = item.get('status', 'not_started')
            if status in user_status_summary:
                user_status_summary[status] += 1
            user_status_summary['total_items'] += 1
    
    context = {
        'user_journals': user_journals,
        'recent_journals': recent_journals,
        'suggested_date_from': week_start,
        'suggested_date_to': week_end,
        'total_journals': WeeklyJournal.objects.count(),
        'user_journal_count': WeeklyJournal.objects.filter(author=request.user).count(),
        'departments': Department.objects.all(),
        'status_summary': status_summary,
        'user_status_summary': user_status_summary,
    }
    
    return render(request, 'journal/dashboard.html', context)

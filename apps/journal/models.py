from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import json


from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import json


class Department(models.Model):
    """Model for different departments in the organization"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class WeeklyJournal(models.Model):
    """Model for weekly team updates/journal entries"""
    
    # Status choices for each item
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'), 
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='journal_entries')
    
    # Date Range
    date_from = models.DateField()
    date_to = models.DateField()
    
    # Journal Content Fields - Using JSON for multiple items with status
    # Each item structure: {"text": "item text", "status": "status_value"}
    highlights = models.JSONField(
        default=list,
        help_text="Key achievements and successes this week"
    )
    pendings = models.JSONField(
        default=list,
        help_text="Tasks and items that are still pending or in progress",
        blank=True
    )
    challenges = models.JSONField(
        default=list,
        help_text="Obstacles, issues, or difficulties encountered",
        blank=True
    )
    personal_updates = models.JSONField(
        default=list,
        help_text="Personal professional development or updates",
        blank=True
    )
    strategies = models.JSONField(
        default=list,
        help_text="Plans, strategies, and next steps for upcoming period",
        blank=True
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_highlights_list(self):
        """Return highlights as a list with status, handling both old text and new JSON format"""
        if isinstance(self.highlights, list):
            result = []
            for item in self.highlights:
                if isinstance(item, dict):
                    # New format with status
                    if item.get('text', '').strip():
                        result.append(item)
                elif isinstance(item, str):
                    # Old format, convert to new format
                    if item.strip():
                        result.append({"text": item.strip(), "status": "completed"})
            return result
        # Very old single text format
        if self.highlights:
            return [{"text": self.highlights, "status": "completed"}]
        return []
    
    def get_pendings_list(self):
        """Return pendings as a list with status, handling both old text and new JSON format"""
        if isinstance(self.pendings, list):
            result = []
            for item in self.pendings:
                if isinstance(item, dict):
                    # New format with status
                    if item.get('text', '').strip():
                        result.append(item)
                elif isinstance(item, str):
                    # Old format, convert to new format
                    if item.strip():
                        result.append({"text": item.strip(), "status": "in_progress"})
            return result
        # Very old single text format
        if self.pendings:
            return [{"text": self.pendings, "status": "in_progress"}]
        return []
    
    def get_challenges_list(self):
        """Return challenges as a list with status, handling both old text and new JSON format"""
        if isinstance(self.challenges, list):
            result = []
            for item in self.challenges:
                if isinstance(item, dict):
                    # New format with status
                    if item.get('text', '').strip():
                        result.append(item)
                elif isinstance(item, str):
                    # Old format, convert to new format
                    if item.strip():
                        result.append({"text": item.strip(), "status": "on_hold"})
            return result
        # Very old single text format
        if self.challenges:
            return [{"text": self.challenges, "status": "on_hold"}]
        return []
    
    def get_personal_updates_list(self):
        """Return personal_updates as a list with status, handling both old text and new JSON format"""
        if isinstance(self.personal_updates, list):
            result = []
            for item in self.personal_updates:
                if isinstance(item, dict):
                    # New format with status
                    if item.get('text', '').strip():
                        result.append(item)
                elif isinstance(item, str):
                    # Old format, convert to new format
                    if item.strip():
                        result.append({"text": item.strip(), "status": "completed"})
            return result
        # Very old single text format
        if self.personal_updates:
            return [{"text": self.personal_updates, "status": "completed"}]
        return []
    
    def get_strategies_list(self):
        """Return strategies as a list with status, handling both old text and new JSON format"""
        if isinstance(self.strategies, list):
            result = []
            for item in self.strategies:
                if isinstance(item, dict):
                    # New format with status
                    if item.get('text', '').strip():
                        result.append(item)
                elif isinstance(item, str):
                    # Old format, convert to new format
                    if item.strip():
                        result.append({"text": item.strip(), "status": "not_started"})
            return result
        # Very old single text format
        if self.strategies:
            return [{"text": self.strategies, "status": "not_started"}]
        return []
    
    @staticmethod
    def get_status_choices():
        """Return available status choices with labels and colors"""
        return [
            ('completed', 'Completed', 'success'),
            ('in_progress', 'In Progress', 'primary'),
            ('on_hold', 'On Hold', 'warning'),
            ('not_started', 'Not Started', 'secondary'),
            ('cancelled', 'Cancelled', 'danger'),
        ]
    
    @staticmethod
    def get_status_display(status):
        """Get display name for status"""
        status_dict = {
            'completed': 'Completed',
            'in_progress': 'In Progress', 
            'on_hold': 'On Hold',
            'not_started': 'Not Started',
            'cancelled': 'Cancelled'
        }
        return status_dict.get(status, status.title())
    
    @staticmethod
    def get_status_color(status):
        """Get Bootstrap color class for status"""
        color_dict = {
            'completed': 'success',
            'in_progress': 'primary',
            'on_hold': 'warning', 
            'not_started': 'secondary',
            'cancelled': 'danger'
        }
        return color_dict.get(status, 'secondary')
    
    def __str__(self):
        return f"{self.author.get_full_name() or self.author.username} - {self.department.name} ({self.date_from} to {self.date_to})"
    
    def get_absolute_url(self):
        return reverse('journal:detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-date_from', '-created_at']
        unique_together = ('author', 'date_from', 'date_to')
        verbose_name = "Weekly Journal Entry"
        verbose_name_plural = "Weekly Journal Entries"


class JournalComment(models.Model):
    """Model for comments on journal entries"""
    journal = models.ForeignKey(WeeklyJournal, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author.get_full_name() or self.author.username} on {self.journal}"
    
    class Meta:
        ordering = ['-created_at']


class TopManagementReport(models.Model):
    """Model for Top Management weekly reports - Admin only"""
    
    title = models.CharField(max_length=200, default="Top Management Weekly Report")
    week_start = models.DateField()
    week_end = models.DateField()
    
    # Admin who created the report
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_reports')
    
    # Additional admin-added items for top management
    admin_highlights = models.JSONField(
        default=list,
        help_text="Additional highlights added directly by admin",
        blank=True
    )
    admin_challenges = models.JSONField(
        default=list,
        help_text="Additional challenges added directly by admin", 
        blank=True
    )
    admin_strategies = models.JSONField(
        default=list,
        help_text="Additional strategies added directly by admin",
        blank=True
    )
    
    # Executive summary
    executive_summary = models.TextField(
        blank=True,
        help_text="Executive summary for top management"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Top Management Report - {self.week_start} to {self.week_end}"
    
    def get_absolute_url(self):
        return reverse('journal:topman_report_detail', kwargs={'pk': self.pk})
    
    def get_all_tagged_items(self):
        """Get all tagged items for this report organized by priority"""
        return self.tagged_items.select_related('journal_entry__author', 'journal_entry__department').order_by('-priority', 'journal_entry__department__name')
    
    def get_tagged_items_by_department(self):
        """Get tagged items organized by department"""
        items = self.get_all_tagged_items()
        departments = {}
        for item in items:
            dept_name = item.get_department_name()
            if dept_name not in departments:
                departments[dept_name] = []
            departments[dept_name].append(item)
        return departments
    
    def get_admin_highlights_list(self):
        """Return admin highlights as a list with status"""
        if isinstance(self.admin_highlights, list):
            return [item for item in self.admin_highlights if isinstance(item, dict) and item.get('text', '').strip()]
        return []
    
    def get_admin_challenges_list(self):
        """Return admin challenges as a list with status"""
        if isinstance(self.admin_challenges, list):
            return [item for item in self.admin_challenges if isinstance(item, dict) and item.get('text', '').strip()]
        return []
    
    def get_admin_strategies_list(self):
        """Return admin strategies as a list with status"""
        if isinstance(self.admin_strategies, list):
            return [item for item in self.admin_strategies if isinstance(item, dict) and item.get('text', '').strip()]
        return []
    
    class Meta:
        ordering = ['-week_start']
        unique_together = ('week_start', 'week_end')
        verbose_name = "Top Management Report"
        verbose_name_plural = "Top Management Reports"


class TopManagementTag(models.Model):
    """Model for tagging journal items for top management visibility"""
    
    # Link to the journal entry
    journal_entry = models.ForeignKey(WeeklyJournal, on_delete=models.CASCADE, related_name='topman_tags')
    
    # Link to the top management report
    report = models.ForeignKey(TopManagementReport, on_delete=models.CASCADE, related_name='tagged_items')
    
    # Which section and item index is tagged
    SECTION_CHOICES = [
        ('highlights', 'Highlights'),
        ('pendings', 'Pendings'),
        ('challenges', 'Challenges'),
        ('personal_updates', 'Personal Updates'),
        ('strategies', 'Strategies'),
    ]
    
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    item_index = models.IntegerField(help_text="Index of the item within the section")
    item_text = models.TextField(help_text="Cached text of the tagged item")
    item_status = models.CharField(max_length=20, help_text="Cached status of the tagged item")
    
    # Admin who tagged the item
    tagged_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tagged_items')
    
    # Optional admin note about why this item is important
    admin_note = models.TextField(
        blank=True,
        help_text="Optional note from admin about this item's importance"
    )
    
    # Priority level for top management attention
    PRIORITY_CHOICES = [
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Metadata
    tagged_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Tagged: {self.item_text[:50]}... - {self.journal_entry.author.username}"
    
    def get_author_name(self):
        """Get the original author's name"""
        return self.journal_entry.author.get_full_name() or self.journal_entry.author.username
    
    def get_department_name(self):
        """Get the department name"""
        return self.journal_entry.department.name
    
    def get_priority_color(self):
        """Get Bootstrap color class for priority"""
        priority_colors = {
            'high': 'danger',
            'medium': 'warning',
            'low': 'info'
        }
        return priority_colors.get(self.priority, 'secondary')
    
    def get_priority_icon(self):
        """Get Font Awesome icon for priority"""
        priority_icons = {
            'high': 'exclamation-triangle',
            'medium': 'info-circle',
            'low': 'check-circle'
        }
        return priority_icons.get(self.priority, 'circle')
    
    class Meta:
        ordering = ['-priority', '-tagged_at']
        unique_together = ('journal_entry', 'section', 'item_index', 'report')
        verbose_name = "Top Management Tag"
        verbose_name_plural = "Top Management Tags"

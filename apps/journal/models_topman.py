# Add these imports to existing imports
from django.contrib.auth.models import User
from django.urls import reverse
import json


# Add this new model after the existing models
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
    
    class Meta:
        ordering = ['-priority', '-tagged_at']
        unique_together = ('journal_entry', 'section', 'item_index', 'report')
        verbose_name = "Top Management Tag"
        verbose_name_plural = "Top Management Tags"

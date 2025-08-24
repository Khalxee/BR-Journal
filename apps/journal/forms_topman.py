from django import forms
from django.forms.widgets import DateInput, Textarea
from .models import TopManagementReport, TopManagementTag, WeeklyJournal
import json
from datetime import date, timedelta


class TopManagementReportForm(forms.ModelForm):
    """Form for creating and editing Top Management reports"""
    
    class Meta:
        model = TopManagementReport
        fields = ['title', 'week_start', 'week_end', 'executive_summary']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Top Management Weekly Report'
            }),
            'week_start': DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'week_end': DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'executive_summary': Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Executive summary for top management...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default dates for current week if creating new report
        if not self.instance.pk:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            self.initial['week_start'] = week_start
            self.initial['week_end'] = week_end
            self.initial['title'] = f"Top Management Report - {week_start.strftime('%B %d')} to {week_end.strftime('%B %d, %Y')}"
        
        # If editing an existing report, populate the dynamic admin fields
        if self.instance.pk:
            self.initial['admin_highlights_data'] = json.dumps(self.instance.get_admin_highlights_list())
            self.initial['admin_challenges_data'] = json.dumps(self.instance.get_admin_challenges_list())
            self.initial['admin_strategies_data'] = json.dumps(self.instance.get_admin_strategies_list())
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('week_start')
        date_to = cleaned_data.get('week_end')
        
        if date_from and date_to:
            if date_from > date_to:
                raise forms.ValidationError("Start date must be before or equal to end date.")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Process dynamic admin fields from POST data
        if hasattr(self, 'data'):
            # Extract admin highlights
            admin_highlights = []
            i = 0
            while f'admin_highlights_{i}' in self.data:
                text = self.data[f'admin_highlights_{i}'].strip()
                status = self.data.get(f'admin_highlights_status_{i}', 'completed')
                if text:
                    admin_highlights.append({"text": text, "status": status})
                i += 1
            instance.admin_highlights = admin_highlights
            
            # Extract admin challenges
            admin_challenges = []
            i = 0
            while f'admin_challenges_{i}' in self.data:
                text = self.data[f'admin_challenges_{i}'].strip()
                status = self.data.get(f'admin_challenges_status_{i}', 'on_hold')
                if text:
                    admin_challenges.append({"text": text, "status": status})
                i += 1
            instance.admin_challenges = admin_challenges
            
            # Extract admin strategies
            admin_strategies = []
            i = 0
            while f'admin_strategies_{i}' in self.data:
                text = self.data[f'admin_strategies_{i}'].strip()
                status = self.data.get(f'admin_strategies_status_{i}', 'not_started')
                if text:
                    admin_strategies.append({"text": text, "status": status})
                i += 1
            instance.admin_strategies = admin_strategies
        
        if commit:
            instance.save()
        return instance


class TopManagementTagForm(forms.ModelForm):
    """Form for tagging journal items for top management"""
    
    class Meta:
        model = TopManagementTag
        fields = ['priority', 'admin_note']
        
        widgets = {
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'admin_note': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional note about why this item is important for top management...'
            }),
        }


class WeekSelectionForm(forms.Form):
    """Form for selecting week range for top management reports"""
    
    week_start = forms.DateField(
        widget=DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Week Start'
    )
    
    week_end = forms.DateField(
        widget=DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Week End'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default dates for current week
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        self.initial['week_start'] = week_start
        self.initial['week_end'] = week_end
    
    def clean(self):
        cleaned_data = super().clean()
        week_start = cleaned_data.get('week_start')
        week_end = cleaned_data.get('week_end')
        
        if week_start and week_end:
            if week_start > week_end:
                raise forms.ValidationError("Start date must be before or equal to end date.")
            
            # Check if date range is reasonable (not too long)
            if (week_end - week_start).days > 14:
                raise forms.ValidationError("Date range should not exceed 2 weeks.")
        
        return cleaned_data

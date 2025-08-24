from django import forms
from django.forms.widgets import DateInput
from .models import WeeklyJournal, JournalComment, Department
import json


class WeeklyJournalForm(forms.ModelForm):
    """Form for creating and editing weekly journal entries with dynamic fields"""
    
    class Meta:
        model = WeeklyJournal
        fields = [
            'department', 'date_from', 'date_to'
        ]
        
        widgets = {
            'date_from': DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'date_to': DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing an existing journal, populate the dynamic fields
        if self.instance.pk:
            # Convert JSON fields back to form data for editing
            self.initial['highlights_data'] = json.dumps(self.instance.get_highlights_list())
            self.initial['pendings_data'] = json.dumps(self.instance.get_pendings_list())
            self.initial['challenges_data'] = json.dumps(self.instance.get_challenges_list())
            self.initial['personal_updates_data'] = json.dumps(self.instance.get_personal_updates_list())
            self.initial['strategies_data'] = json.dumps(self.instance.get_strategies_list())
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to:
            if date_from > date_to:
                raise forms.ValidationError("Start date must be before or equal to end date.")
        
        # Validate that at least one highlight is provided
        if hasattr(self, 'data'):
            highlights = []
            i = 0
            while f'highlights_{i}' in self.data:
                text = self.data[f'highlights_{i}'].strip()
                if text:
                    highlights.append(text)
                i += 1
            
            if not highlights:
                raise forms.ValidationError("At least one highlight is required.")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Process dynamic fields from POST data with status
        if hasattr(self, 'data'):
            # Extract highlights
            highlights = []
            i = 0
            while f'highlights_{i}' in self.data:
                text = self.data[f'highlights_{i}'].strip()
                status = self.data.get(f'highlights_status_{i}', 'completed')
                if text:
                    highlights.append({"text": text, "status": status})
                i += 1
            instance.highlights = highlights
            
            # Extract pendings
            pendings = []
            i = 0
            while f'pendings_{i}' in self.data:
                text = self.data[f'pendings_{i}'].strip()
                status = self.data.get(f'pendings_status_{i}', 'in_progress')
                if text:
                    pendings.append({"text": text, "status": status})
                i += 1
            instance.pendings = pendings
            
            # Extract challenges
            challenges = []
            i = 0
            while f'challenges_{i}' in self.data:
                text = self.data[f'challenges_{i}'].strip()
                status = self.data.get(f'challenges_status_{i}', 'on_hold')
                if text:
                    challenges.append({"text": text, "status": status})
                i += 1
            instance.challenges = challenges
            
            # Extract personal_updates
            personal_updates = []
            i = 0
            while f'personal_updates_{i}' in self.data:
                text = self.data[f'personal_updates_{i}'].strip()
                status = self.data.get(f'personal_updates_status_{i}', 'completed')
                if text:
                    personal_updates.append({"text": text, "status": status})
                i += 1
            instance.personal_updates = personal_updates
            
            # Extract strategies
            strategies = []
            i = 0
            while f'strategies_{i}' in self.data:
                text = self.data[f'strategies_{i}'].strip()
                status = self.data.get(f'strategies_status_{i}', 'not_started')
                if text:
                    strategies.append({"text": text, "status": status})
                i += 1
            instance.strategies = strategies
        
        if commit:
            instance.save()
        return instance


class JournalCommentForm(forms.ModelForm):
    """Form for adding comments to journal entries"""
    
    class Meta:
        model = JournalComment
        fields = ['content']
        
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add your comment...'
            })
        }

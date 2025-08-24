from django import template
from apps.journal.models import WeeklyJournal

register = template.Library()

@register.filter
def get_status_display(status):
    """Get display name for status"""
    return WeeklyJournal.get_status_display(status)

@register.filter
def get_status_color(status):
    """Get Bootstrap color class for status"""
    return WeeklyJournal.get_status_color(status)

@register.filter
def get_status_icon(status):
    """Get Font Awesome icon for status"""
    icon_dict = {
        'completed': 'check-circle',
        'in_progress': 'clock',
        'on_hold': 'pause-circle',
        'not_started': 'circle',
        'cancelled': 'times-circle'
    }
    return icon_dict.get(status, 'circle')

@register.filter
def count_by_status(items, status):
    """Count items by their status"""
    if not items:
        return 0
    count = 0
    for item in items:
        if isinstance(item, dict) and item.get('status') == status:
            count += 1
        elif hasattr(item, 'status') and item.status == status:
            count += 1
    return count

@register.filter
def count_by_priority(items, priority):
    """Count tagged items by their priority level"""
    if not items:
        return 0
    count = 0
    for item in items:
        if hasattr(item, 'priority') and item.priority == priority:
            count += 1
    return count

@register.filter
def get_all_statuses():
    """Get all status choices"""
    return WeeklyJournal.get_status_choices()

@register.simple_tag
def get_status_summary(journal):
    """Get complete status summary for a journal entry"""
    all_items = []
    all_items.extend(journal.get_highlights_list())
    all_items.extend(journal.get_pendings_list())
    all_items.extend(journal.get_challenges_list())
    all_items.extend(journal.get_personal_updates_list())
    all_items.extend(journal.get_strategies_list())
    
    summary = {
        'completed': 0,
        'in_progress': 0,
        'on_hold': 0,
        'not_started': 0,
        'cancelled': 0,
        'total': len(all_items)
    }
    
    for item in all_items:
        status = item.get('status', 'not_started')
        if status in summary:
            summary[status] += 1
    
    return summary

@register.filter  
def filter_by_priority(items, priority):
    """Filter tagged items by priority level"""
    return [item for item in items if item.priority == priority]

@register.filter
def filter_by_department(items, department_name):
    """Filter tagged items by department name"""
    return [item for item in items if item.get_department_name() == department_name]

@register.filter
def regroup_by(items, attribute):
    """Regroup items by an attribute for counting"""
    from django.template.defaultfilters import dictsort
    groups = {}
    for item in items:
        key = getattr(item, attribute, 'Unknown')
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

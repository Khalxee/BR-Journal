from django.contrib import admin
from django.utils.html import format_html
from .models import Department, WeeklyJournal, JournalComment, TopManagementReport, TopManagementTag


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


class JournalCommentInline(admin.TabularInline):
    model = JournalComment
    extra = 0
    readonly_fields = ('author', 'created_at')


@admin.register(WeeklyJournal)
class WeeklyJournalAdmin(admin.ModelAdmin):
    list_display = ('author', 'department', 'date_from', 'date_to', 'created_at')
    list_filter = ('department', 'date_from', 'created_at', 'author')
    search_fields = ('author__username', 'author__first_name', 'author__last_name', 
                     'department__name', 'highlights', 'challenges')
    date_hierarchy = 'date_from'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('author', 'department', 'date_from', 'date_to')
        }),
        ('Journal Content', {
            'fields': ('highlights', 'pendings', 'challenges', 'personal_updates', 'strategies'),
            'classes': ('wide',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [JournalCommentInline]


@admin.register(JournalComment)
class JournalCommentAdmin(admin.ModelAdmin):
    list_display = ('journal', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'journal__author__username')
    readonly_fields = ('created_at',)


class TopManagementTagInline(admin.TabularInline):
    model = TopManagementTag
    extra = 0
    readonly_fields = ('tagged_by', 'tagged_at', 'journal_entry', 'section', 'item_index', 'item_text', 'item_status')
    fields = ('journal_entry', 'section', 'item_text', 'item_status', 'priority', 'admin_note', 'tagged_by', 'tagged_at')
    

@admin.register(TopManagementReport)
class TopManagementReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'week_start', 'week_end', 'created_by', 'tagged_items_count', 'created_at')
    list_filter = ('week_start', 'created_by', 'created_at')
    search_fields = ('title', 'executive_summary', 'created_by__username')
    date_hierarchy = 'week_start'
    readonly_fields = ('created_by', 'created_at', 'updated_at', 'tagged_items_count')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('title', 'week_start', 'week_end', 'created_by', 'tagged_items_count')
        }),
        ('Executive Summary', {
            'fields': ('executive_summary',),
            'classes': ('wide',)
        }),
        ('Admin Added Items', {
            'fields': ('admin_highlights', 'admin_challenges', 'admin_strategies'),
            'classes': ('collapse', 'wide'),
            'description': 'Additional items added directly by admin for top management attention'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [TopManagementTagInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def tagged_items_count(self, obj):
        """Display number of tagged items"""
        count = obj.tagged_items.count()
        return format_html('<span class="badge" style="background-color: #007bff; color: white;">{}</span>', count)
    tagged_items_count.short_description = 'Tagged Items'
    
    def has_add_permission(self, request):
        """Only superusers and staff can add top management reports"""
        return request.user.is_superuser or request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        """Only superusers and staff can change top management reports"""
        return request.user.is_superuser or request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete top management reports"""
        return request.user.is_superuser


@admin.register(TopManagementTag)
class TopManagementTagAdmin(admin.ModelAdmin):
    list_display = ('journal_entry_info', 'section', 'item_text_short', 'priority', 'tagged_by', 'report', 'tagged_at')
    list_filter = ('section', 'priority', 'tagged_by', 'report__week_start', 'tagged_at')
    search_fields = ('item_text', 'admin_note', 'journal_entry__author__username', 'tagged_by__username')
    readonly_fields = ('tagged_by', 'tagged_at', 'journal_entry', 'section', 'item_index', 'item_text', 'item_status')
    
    fieldsets = (
        ('Tagged Item Information', {
            'fields': ('journal_entry', 'section', 'item_index', 'item_text', 'item_status')
        }),
        ('Tagging Information', {
            'fields': ('report', 'priority', 'admin_note', 'tagged_by', 'tagged_at')
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.tagged_by = request.user
        super().save_model(request, obj, form, change)
    
    def journal_entry_info(self, obj):
        """Display journal entry information"""
        return format_html(
            '<strong>{}</strong><br><small>{} - {} to {}</small>',
            obj.get_author_name(),
            obj.get_department_name(),
            obj.journal_entry.date_from,
            obj.journal_entry.date_to
        )
    journal_entry_info.short_description = 'Journal Entry'
    
    def item_text_short(self, obj):
        """Display shortened item text"""
        text = obj.item_text[:80] + '...' if len(obj.item_text) > 80 else obj.item_text
        return format_html('<span title="{}">{}</span>', obj.item_text, text)
    item_text_short.short_description = 'Item Text'
    
    def has_add_permission(self, request):
        """Only superusers and staff can add tags"""
        return request.user.is_superuser or request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        """Only superusers and staff can change tags"""
        return request.user.is_superuser or request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers and staff can delete tags"""
        return request.user.is_superuser or request.user.is_staff

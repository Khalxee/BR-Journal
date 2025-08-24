from django.contrib import admin
from .models import (
    Document, DocumentTemplate, Letterhead, DocumentType, 
    Signatory, QRCode, DocumentHistory
)


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Letterhead)
class LetterheadAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'company_name')


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Signatory)
class SignatoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'department', 'is_active', 'created_at')
    list_filter = ('is_active', 'department', 'created_at')
    search_fields = ('name', 'title', 'department')


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'qr_type', 'is_active', 'created_at')
    list_filter = ('qr_type', 'is_active', 'created_at')
    search_fields = ('name', 'content')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'document_type', 'created_at')
    search_fields = ('title', 'addressee_name', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(created_by=request.user)
        return qs


@admin.register(DocumentHistory)
class DocumentHistoryAdmin(admin.ModelAdmin):
    list_display = ('document', 'action', 'user', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('document__title', 'user__username', 'description')
    readonly_fields = ('timestamp',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(document__created_by=request.user)
        return qs

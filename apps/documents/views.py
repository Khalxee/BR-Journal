from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import (
    Document, DocumentTemplate, Letterhead, DocumentType, 
    Signatory, QRCode, DocumentHistory
)
import json


@login_required
def document_list(request):
    """List all documents for the current user"""
    documents = Document.objects.filter(created_by=request.user)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        documents = documents.filter(
            Q(title__icontains=search) |
            Q(addressee_name__icontains=search) |
            Q(document_type__name__icontains=search)
        )
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        documents = documents.filter(status=status)
    
    # Pagination
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'documents': page_obj,
        'search': search,
        'status': status,
        'status_choices': Document.STATUS_CHOICES,
    }
    return render(request, 'documents/list.html', context)


@login_required
def create_document(request):
    """Create a new document"""
    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title')
            document_type_id = request.POST.get('document_type')
            letterhead_id = request.POST.get('letterhead')
            date = request.POST.get('date')
            addressee_name = request.POST.get('addressee_name')
            addressee_address = request.POST.get('addressee_address')
            body = request.POST.get('body')
            salutation = request.POST.get('salutation', 'Sincerely')
            signatory_id = request.POST.get('signatory')
            qr_code_id = request.POST.get('qr_code')
            action = request.POST.get('action', 'save_draft')
            
            # Create document
            document = Document.objects.create(
                title=title,
                document_type_id=document_type_id,
                letterhead_id=letterhead_id,
                date=date,
                addressee_name=addressee_name,
                addressee_address=addressee_address,
                body=body,
                salutation=salutation,
                signatory_id=signatory_id if signatory_id else None,
                qr_code_id=qr_code_id if qr_code_id else None,
                status='draft' if action == 'save_draft' else 'sent',
                created_by=request.user
            )
            
            # Log action
            DocumentHistory.objects.create(
                document=document,
                action='created',
                description=f'Document created as {document.status}',
                user=request.user
            )
            
            if action == 'save_draft':
                messages.success(request, f'Document "{title}" saved as draft.')
                return redirect('document_detail', pk=document.pk)
            elif action == 'send_email':
                # TODO: Implement email sending
                messages.success(request, f'Document "{title}" has been sent via email.')
                return redirect('document_detail', pk=document.pk)
            elif action == 'export':
                # TODO: Implement PDF export
                messages.success(request, f'Document "{title}" exported successfully.')
                return redirect('export_document', pk=document.pk)
            
        except Exception as e:
            messages.error(request, f'Error creating document: {str(e)}')
    
    # Get form data
    context = {
        'document_types': DocumentType.objects.filter(is_active=True),
        'letterheads': Letterhead.objects.filter(is_active=True),
        'signatories': Signatory.objects.filter(is_active=True),
        'qr_codes': QRCode.objects.filter(is_active=True),
    }
    return render(request, 'documents/create.html', context)


@login_required
def document_detail(request, pk):
    """View document details"""
    document = get_object_or_404(Document, pk=pk, created_by=request.user)
    
    # Log view action
    DocumentHistory.objects.create(
        document=document,
        action='viewed',
        description='Document viewed',
        user=request.user
    )
    
    return render(request, 'documents/detail.html', {'document': document})


@login_required
def edit_document(request, pk):
    """Edit an existing document"""
    document = get_object_or_404(Document, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        try:
            # Update document fields
            document.title = request.POST.get('title')
            document.document_type_id = request.POST.get('document_type')
            document.letterhead_id = request.POST.get('letterhead')
            document.date = request.POST.get('date')
            document.addressee_name = request.POST.get('addressee_name')
            document.addressee_address = request.POST.get('addressee_address')
            document.body = request.POST.get('body')
            document.salutation = request.POST.get('salutation')
            
            signatory_id = request.POST.get('signatory')
            document.signatory_id = signatory_id if signatory_id else None
            
            qr_code_id = request.POST.get('qr_code')
            document.qr_code_id = qr_code_id if qr_code_id else None
            
            document.save()
            
            # Log action
            DocumentHistory.objects.create(
                document=document,
                action='updated',
                description='Document updated',
                user=request.user
            )
            
            messages.success(request, f'Document "{document.title}" updated successfully.')
            return redirect('document_detail', pk=document.pk)
            
        except Exception as e:
            messages.error(request, f'Error updating document: {str(e)}')
    
    context = {
        'document': document,
        'document_types': DocumentType.objects.filter(is_active=True),
        'letterheads': Letterhead.objects.filter(is_active=True),
        'signatories': Signatory.objects.filter(is_active=True),
        'qr_codes': QRCode.objects.filter(is_active=True),
    }
    return render(request, 'documents/edit.html', context)


@login_required
def delete_document(request, pk):
    """Delete a document"""
    document = get_object_or_404(Document, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        title = document.title
        
        # Log deletion
        DocumentHistory.objects.create(
            document=document,
            action='deleted',
            description='Document deleted',
            user=request.user
        )
        
        document.delete()
        messages.success(request, f'Document "{title}" deleted successfully.')
        return redirect('document_list')
    
    return render(request, 'documents/delete_confirm.html', {'document': document})


@login_required
def export_document(request, pk):
    """Export document as PDF"""
    document = get_object_or_404(Document, pk=pk, created_by=request.user)
    
    # Log export action
    DocumentHistory.objects.create(
        document=document,
        action='exported',
        description='Document exported as PDF',
        user=request.user
    )
    
    # TODO: Implement actual PDF generation
    # For now, return a placeholder response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.title}.pdf"'
    response.write(b'PDF content would be generated here')
    
    return response


@login_required
def email_document(request, pk):
    """Send document via email"""
    document = get_object_or_404(Document, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        email_to = request.POST.get('email_to')
        email_subject = request.POST.get('email_subject')
        email_message = request.POST.get('email_message')
        
        # TODO: Implement actual email sending
        # For now, just log the action
        DocumentHistory.objects.create(
            document=document,
            action='sent',
            description=f'Document sent via email to {email_to}',
            user=request.user
        )
        
        document.status = 'sent'
        document.save()
        
        messages.success(request, f'Document "{document.title}" sent to {email_to}.')
        return redirect('document_detail', pk=document.pk)
    
    context = {
        'document': document,
        'default_subject': f'Document: {document.title}',
        'default_message': f'Please find attached the document "{document.title}".',
    }
    return render(request, 'documents/email.html', context)


@login_required
def document_history(request):
    """View document history"""
    history = DocumentHistory.objects.filter(document__created_by=request.user)
    
    # Filter by action
    action = request.GET.get('action')
    if action:
        history = history.filter(action=action)
    
    # Search
    search = request.GET.get('search')
    if search:
        history = history.filter(
            Q(document__title__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(history, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'history': page_obj,
        'action_choices': DocumentHistory.ACTION_CHOICES,
        'search': search,
        'action': action,
    }
    return render(request, 'documents/history.html', context)


# Settings Management Views
@login_required
def settings_dashboard(request):
    """Settings dashboard"""
    context = {
        'templates_count': DocumentTemplate.objects.filter(is_active=True).count(),
        'letterheads_count': Letterhead.objects.filter(is_active=True).count(),
        'document_types_count': DocumentType.objects.filter(is_active=True).count(),
        'signatories_count': Signatory.objects.filter(is_active=True).count(),
        'qrcodes_count': QRCode.objects.filter(is_active=True).count(),
    }
    return render(request, 'documents/settings/dashboard.html', context)


@login_required
def manage_templates(request):
    """Manage document templates"""
    templates = DocumentTemplate.objects.all()
    return render(request, 'documents/settings/templates.html', {'templates': templates})


@login_required
def manage_letterheads(request):
    """Manage letterheads"""
    letterheads = Letterhead.objects.all()
    return render(request, 'documents/settings/letterheads.html', {'letterheads': letterheads})


@login_required
def manage_document_types(request):
    """Manage document types"""
    document_types = DocumentType.objects.all()
    return render(request, 'documents/settings/document_types.html', {'document_types': document_types})


@login_required
def manage_signatories(request):
    """Manage signatories"""
    signatories = Signatory.objects.all()
    return render(request, 'documents/settings/signatories.html', {'signatories': signatories})


@login_required
def manage_qrcodes(request):
    """Manage QR codes"""
    qrcodes = QRCode.objects.all()
    return render(request, 'documents/settings/qrcodes.html', {'qrcodes': qrcodes})


# User Management (Admin Only)
@staff_member_required
def user_management(request):
    """User management dashboard (admin only)"""
    users = User.objects.all().order_by('-date_joined')
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'search': search,
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'staff_users': User.objects.filter(is_staff=True).count(),
    }
    return render(request, 'documents/user_management.html', context)

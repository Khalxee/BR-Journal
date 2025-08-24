"""
Admin-specific views for DocuApp user management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime, timedelta
from django.utils import timezone


def is_admin_user(user):
    """Check if user is admin (staff or superuser)"""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin_user, login_url='dashboard')
def user_management(request):
    """Main user management page"""
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    role_filter = request.GET.get('role', 'all')
    
    # Base queryset
    users = User.objects.all().order_by('-date_joined')
    
    # Apply search filter
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # Apply role filter
    if role_filter == 'admin':
        users = users.filter(Q(is_staff=True) | Q(is_superuser=True))
    elif role_filter == 'user':
        users = users.filter(is_staff=False, is_superuser=False)
    
    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    admin_users = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).count()
    recent_users = User.objects.filter(
        date_joined__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'role_filter': role_filter,
        'total_users': total_users,
        'active_users': active_users,
        'admin_users': admin_users,
        'recent_users': recent_users,
        'is_admin': True,
    }
    
    return render(request, 'web/admin/user_management.html', context)


@login_required
@user_passes_test(is_admin_user, login_url='dashboard')
def create_user(request):
    """Create new user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        is_active = request.POST.get('is_active', 'on') == 'on'
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'web/admin/create_user.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'web/admin/create_user.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'web/admin/create_user.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_superuser=is_superuser,
                is_active=is_active
            )
            
            messages.success(request, f'User "{username}" created successfully!')
            return redirect('user_management')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return render(request, 'web/admin/create_user.html')


@login_required
@user_passes_test(is_admin_user, login_url='dashboard')
def edit_user(request, user_id):
    """Edit existing user"""
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        
        # Validation
        if password and password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'web/admin/edit_user.html', {'user_to_edit': user_to_edit})
        
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'web/admin/edit_user.html', {'user_to_edit': user_to_edit})
        
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'web/admin/edit_user.html', {'user_to_edit': user_to_edit})
        
        try:
            user_to_edit.username = username
            user_to_edit.email = email
            user_to_edit.first_name = first_name
            user_to_edit.last_name = last_name
            user_to_edit.is_staff = is_staff
            user_to_edit.is_superuser = is_superuser
            user_to_edit.is_active = is_active
            
            if password:
                user_to_edit.set_password(password)
            
            user_to_edit.save()
            
            messages.success(request, f'User "{username}" updated successfully!')
            return redirect('user_management')
            
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    return render(request, 'web/admin/edit_user.html', {'user_to_edit': user_to_edit})


@login_required
@user_passes_test(is_admin_user, login_url='dashboard')
def user_details(request, user_id):
    """View user details"""
    user_to_view = get_object_or_404(User, id=user_id)
    
    # Get user's login history (last 10 logins)
    # This would require a custom model to track login history
    # For now, we'll show basic information
    
    context = {
        'user_to_view': user_to_view,
        'is_admin': True,
    }
    
    return render(request, 'web/admin/user_details.html', context)


@csrf_exempt
@login_required
@user_passes_test(is_admin_user, login_url='dashboard')
@require_http_methods(["POST"])
def toggle_user_status(request):
    """Toggle user active/inactive status via AJAX"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        user_to_toggle = get_object_or_404(User, id=user_id)
        
        # Don't allow deactivating self
        if user_to_toggle == request.user:
            return JsonResponse({
                'success': False, 
                'message': 'You cannot deactivate your own account.'
            })
        
        user_to_toggle.is_active = not user_to_toggle.is_active
        user_to_toggle.save()
        
        status = 'activated' if user_to_toggle.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'User "{user_to_toggle.username}" {status} successfully.',
            'new_status': user_to_toggle.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })


@csrf_exempt
@login_required
@user_passes_test(is_admin_user, login_url='dashboard')
@require_http_methods(["POST"])
def delete_user(request):
    """Delete user via AJAX"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        user_to_delete = get_object_or_404(User, id=user_id)
        
        # Don't allow deleting self
        if user_to_delete == request.user:
            return JsonResponse({
                'success': False, 
                'message': 'You cannot delete your own account.'
            })
        
        username = user_to_delete.username
        user_to_delete.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'User "{username}" deleted successfully.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })


@login_required
@user_passes_test(is_admin_user, login_url='dashboard')
def reset_user_password(request, user_id):
    """Reset user password"""
    user_to_reset = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'web/admin/reset_password.html', {'user_to_reset': user_to_reset})
        
        try:
            user_to_reset.set_password(new_password)
            user_to_reset.save()
            
            messages.success(request, f'Password reset successfully for user "{user_to_reset.username}"!')
            return redirect('user_management')
            
        except Exception as e:
            messages.error(request, f'Error resetting password: {str(e)}')
    
    return render(request, 'web/admin/reset_password.html', {'user_to_reset': user_to_reset})


@login_required
@user_passes_test(is_admin_user, login_url='dashboard')
def create_admin_account(request):
    """Create a new admin account"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        admin_type = request.POST.get('admin_type', 'staff')  # 'staff' or 'superuser'
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'web/admin/create_admin.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'web/admin/create_admin.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'web/admin/create_admin.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                is_superuser=(admin_type == 'superuser'),
                is_active=True
            )
            
            admin_title = 'Super Administrator' if admin_type == 'superuser' else 'Administrator'
            messages.success(request, f'{admin_title} "{username}" created successfully!')
            return redirect('user_management')
            
        except Exception as e:
            messages.error(request, f'Error creating admin: {str(e)}')
    
    return render(request, 'web/admin/create_admin.html')

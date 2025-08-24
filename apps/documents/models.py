from django.db import models
from django.contrib.auth.models import User


class DocumentTemplate(models.Model):
    """Document templates for different types of documents"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    template_content = models.TextField(help_text="HTML template with placeholders")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Letterhead(models.Model):
    """Company letterheads"""
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='letterheads/', blank=True, null=True)
    company_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    header_html = models.TextField(help_text="Custom HTML for header")
    footer_html = models.TextField(blank=True, help_text="Custom HTML for footer")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class DocumentType(models.Model):
    """Types of documents that can be created"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    default_template = models.ForeignKey(DocumentTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Signatory(models.Model):
    """People who can sign documents"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    signature_image = models.ImageField(upload_to='signatures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.title}"


class QRCode(models.Model):
    """QR Code configurations for documents"""
    name = models.CharField(max_length=100)
    qr_type = models.CharField(max_length=50, choices=[
        ('url', 'Website URL'),
        ('email', 'Email'),
        ('text', 'Plain Text'),
        ('verification', 'Document Verification')
    ])
    content = models.TextField(help_text="Content to encode in QR code")
    size = models.IntegerField(default=100, help_text="QR code size in pixels")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Document(models.Model):
    """Documents created by users"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    letterhead = models.ForeignKey(Letterhead, on_delete=models.CASCADE)
    template = models.ForeignKey(DocumentTemplate, on_delete=models.CASCADE, null=True, blank=True)
    
    # Document content
    date = models.DateField()
    addressee_name = models.CharField(max_length=200)
    addressee_address = models.TextField()
    body = models.TextField()
    salutation = models.CharField(max_length=100, default="Sincerely")
    
    # Signature and QR
    signatory = models.ForeignKey(Signatory, on_delete=models.CASCADE, null=True, blank=True)
    qr_code = models.ForeignKey(QRCode, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Document management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Generated content
    generated_html = models.TextField(blank=True, help_text="Final generated HTML")
    pdf_file = models.FileField(upload_to='documents/pdf/', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.status})"


class DocumentHistory(models.Model):
    """Track document actions and changes"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('sent', 'Sent via Email'),
        ('exported', 'Exported'),
        ('deleted', 'Deleted'),
        ('viewed', 'Viewed'),
    ]
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.document.title} - {self.action} by {self.user.username}"

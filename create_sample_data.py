#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/Users/beverlybabida/Desktop/bbc projects/docuapp')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docuapp.settings')
django.setup()

from apps.documents.models import DocumentType, Letterhead, Signatory, QRCode, DocumentTemplate
from django.contrib.auth.models import User

def create_sample_data():
    print("Creating sample data...")
    
    # Get or create a user for created_by fields
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@docuapp.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        user.set_password('admin123')
        user.save()
        print("Created admin user")
    
    # Create document types
    doc_types = [
        {'name': 'Business Letter', 'description': 'Standard business correspondence'},
        {'name': 'Official Memo', 'description': 'Internal office memorandum'},
        {'name': 'Invoice', 'description': 'Billing document'},
        {'name': 'Certificate', 'description': 'Official certification document'},
        {'name': 'Report', 'description': 'Formal report document'}
    ]
    
    for dt in doc_types:
        obj, created = DocumentType.objects.get_or_create(
            name=dt['name'], 
            defaults={'description': dt['description']}
        )
        if created:
            print(f"Created document type: {dt['name']}")
    
    # Create letterheads
    letterhead, created = Letterhead.objects.get_or_create(
        name='Company Letterhead',
        defaults={
            'company_name': 'DocuApp Inc.',
            'address': '123 Business Street\nSuite 100\nCity, State 12345',
            'phone': '+1 (555) 123-4567',
            'email': 'info@docuapp.com',
            'website': 'https://docuapp.com',
            'header_html': '<div style="text-align: center; border-bottom: 2px solid #667eea; padding: 20px;"><h1 style="color: #667eea;">DocuApp Inc.</h1><p>Professional Document Solutions</p></div>',
            'footer_html': '<div style="text-align: center; border-top: 1px solid #ccc; padding: 10px; font-size: 12px;">DocuApp Inc. | 123 Business Street | info@docuapp.com</div>'
        }
    )
    if created:
        print("Created company letterhead")
    
    # Create signatories
    signatories = [
        {'name': 'John Smith', 'title': 'CEO', 'department': 'Executive'},
        {'name': 'Jane Doe', 'title': 'HR Manager', 'department': 'Human Resources'},
        {'name': 'Mike Johnson', 'title': 'CFO', 'department': 'Finance'}
    ]
    
    for sig in signatories:
        obj, created = Signatory.objects.get_or_create(
            name=sig['name'],
            defaults=sig
        )
        if created:
            print(f"Created signatory: {sig['name']}")
    
    # Create QR codes
    qr_codes = [
        {'name': 'Company Website', 'qr_type': 'url', 'content': 'https://docuapp.com'},
        {'name': 'Contact Email', 'qr_type': 'email', 'content': 'info@docuapp.com'},
        {'name': 'Document Verification', 'qr_type': 'verification', 'content': 'Verify at https://docuapp.com/verify'}
    ]
    
    for qr in qr_codes:
        obj, created = QRCode.objects.get_or_create(
            name=qr['name'],
            defaults=qr
        )
        if created:
            print(f"Created QR code: {qr['name']}")
    
    # Create document templates
    template, created = DocumentTemplate.objects.get_or_create(
        name='Basic Business Letter',
        defaults={
            'description': 'Standard business letter template',
            'template_content': '''
            <div class="document">
                <div class="header">{{ letterhead.header_html|safe }}</div>
                <div class="content">
                    <p class="date">{{ date }}</p>
                    <div class="addressee">
                        <p><strong>{{ addressee_name }}</strong></p>
                        <p>{{ addressee_address|linebreaks }}</p>
                    </div>
                    <div class="body">
                        {{ body|linebreaks }}
                    </div>
                    <div class="signature">
                        <p>{{ salutation }},</p>
                        {% if signatory %}
                        <br><br>
                        <p><strong>{{ signatory.name }}</strong></p>
                        <p>{{ signatory.title }}</p>
                        {% endif %}
                    </div>
                </div>
                <div class="footer">{{ letterhead.footer_html|safe }}</div>
            </div>
            ''',
            'created_by': user
        }
    )
    if created:
        print("Created basic business letter template")
    
    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data()

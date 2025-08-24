from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.journal.models import Department, WeeklyJournal, TopManagementReport, TopManagementTag
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create sample Top Management data and make admin user'

    def handle(self, *args, **options):
        # Create or update admin user to have staff privileges
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        
        if not created:
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.first_name = 'Admin'
            admin_user.last_name = 'User'
            admin_user.save()
        
        admin_user.set_password('admin123')
        admin_user.save()
        
        # Make john_doe a staff member too for testing
        try:
            john = User.objects.get(username='john_doe')
            john.is_staff = True
            john.save()
            self.stdout.write(self.style.SUCCESS(f'Made john_doe a staff member'))
        except User.DoesNotExist:
            pass
        
        # Get current week dates
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Previous week dates  
        prev_week_start = week_start - timedelta(days=7)
        prev_week_end = prev_week_start + timedelta(days=6)
        
        # Create sample Top Management reports
        current_report, created = TopManagementReport.objects.get_or_create(
            week_start=week_start,
            week_end=week_end,
            defaults={
                'created_by': admin_user,
                'title': f"Executive Summary - {week_start.strftime('%B %d')} to {week_end.strftime('%B %d, %Y')}",
                'executive_summary': """Key highlights this week include successful deployment of the authentication system and resolution of critical payment processing issues. Engineering team delivered ahead of schedule.

Marketing campaign launch exceeded expectations with 25% increase in email engagement. New customer acquisition up 15% week-over-week.

Critical challenges remain around server capacity and database optimization. Immediate attention needed for infrastructure scaling.""",
                'admin_highlights': [
                    {"text": "Successfully launched Q4 strategic initiative ahead of schedule", "status": "completed"},
                    {"text": "Secured partnership with major enterprise client", "status": "completed"},
                    {"text": "Revenue targets exceeded by 12% for the quarter", "status": "completed"}
                ],
                'admin_challenges': [
                    {"text": "Infrastructure scaling needed for increased load", "status": "in_progress"},
                    {"text": "Budget allocation pending for new hiring initiatives", "status": "on_hold"}
                ],
                'admin_strategies': [
                    {"text": "Plan expansion into European market Q1 2026", "status": "not_started"},
                    {"text": "Evaluate acquisition targets in AI/ML space", "status": "not_started"}
                ]
            }
        )
        
        previous_report, created = TopManagementReport.objects.get_or_create(
            week_start=prev_week_start,
            week_end=prev_week_end,
            defaults={
                'created_by': admin_user,
                'title': f"Executive Summary - {prev_week_start.strftime('%B %d')} to {prev_week_end.strftime('%B %d, %Y')}",
                'executive_summary': """Previous week focused on preparing for Q4 launch. Engineering completed major milestone with CI/CD pipeline deployment.

Marketing team preparing campaign materials and vendor negotiations ongoing. Sales team building pipeline for Q4 push.

Key challenges include resource allocation and timeline management for multiple concurrent projects.""",
                'admin_highlights': [
                    {"text": "Completed security audit with zero critical findings", "status": "completed"},
                    {"text": "Onboarded 3 senior engineers ahead of schedule", "status": "completed"}
                ],
                'admin_challenges': [
                    {"text": "Cross-team coordination needs improvement", "status": "on_hold"},
                    {"text": "Remote work policies need standardization", "status": "in_progress"}
                ],
                'admin_strategies': [
                    {"text": "Implement new project management framework", "status": "in_progress"},
                    {"text": "Establish quarterly all-hands meetings", "status": "completed"}
                ]
            }
        )
        
        # Create sample tags for journal entries if they exist
        journal_entries = WeeklyJournal.objects.filter(
            date_from__lte=week_end,
            date_to__gte=week_start
        )
        
        tagged_count = 0
        for journal in journal_entries:
            # Tag some highlights as high priority
            highlights = journal.get_highlights_list()
            if highlights:
                for i, highlight in enumerate(highlights[:2]):  # Tag first 2 highlights
                    if 'authentication' in highlight.get('text', '').lower() or 'critical' in highlight.get('text', '').lower():
                        tag, tag_created = TopManagementTag.objects.get_or_create(
                            journal_entry=journal,
                            report=current_report,
                            section='highlights',
                            item_index=i,
                            defaults={
                                'item_text': highlight.get('text', ''),
                                'item_status': highlight.get('status', 'completed'),
                                'tagged_by': admin_user,
                                'priority': 'high',
                                'admin_note': 'Critical system component - requires executive visibility'
                            }
                        )
                        if tag_created:
                            tagged_count += 1
            
            # Tag some challenges as medium/high priority
            challenges = journal.get_challenges_list()
            if challenges:
                for i, challenge in enumerate(challenges[:1]):  # Tag first challenge
                    tag, tag_created = TopManagementTag.objects.get_or_create(
                        journal_entry=journal,
                        report=current_report,
                        section='challenges',
                        item_index=i,
                        defaults={
                            'item_text': challenge.get('text', ''),
                            'item_status': challenge.get('status', 'on_hold'),
                            'tagged_by': admin_user,
                            'priority': 'medium',
                            'admin_note': 'Potential risk that needs management attention'
                        }
                    )
                    if tag_created:
                        tagged_count += 1
        
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('=== Top Management System Setup Complete! ==='))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Admin Users:'))
        self.stdout.write(self.style.SUCCESS(f'  - admin / admin123 (superuser)'))
        if User.objects.filter(username='john_doe', is_staff=True).exists():
            self.stdout.write(self.style.SUCCESS(f'  - john_doe / password123 (staff)'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Created Reports:'))
        self.stdout.write(self.style.SUCCESS(f'  - Current Week: {week_start} to {week_end}'))
        self.stdout.write(self.style.SUCCESS(f'  - Previous Week: {prev_week_start} to {prev_week_end}'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS(f'Tagged Items: {tagged_count} journal items tagged for executive attention'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('🎯 Top Management Features Available:'))
        self.stdout.write(self.style.SUCCESS('   📊 Executive Reports - Create and manage weekly reports'))
        self.stdout.write(self.style.SUCCESS('   🏷️  Item Tagging - Flag important items for executive visibility'))
        self.stdout.write(self.style.SUCCESS('   📈 Weekly Analytics - Comprehensive status tracking and insights'))
        self.stdout.write(self.style.SUCCESS('   ⚡ Admin Tools - Add items directly to executive reports'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Access Top Management features:'))
        self.stdout.write(self.style.SUCCESS('  1. Login as admin user'))
        self.stdout.write(self.style.SUCCESS('  2. Look for "Top Management" section in sidebar'))
        self.stdout.write(self.style.SUCCESS('  3. Navigate to Reports, Tag Items, or Weekly Summary'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Run: python3 manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('Visit: http://127.0.0.1:8000/'))

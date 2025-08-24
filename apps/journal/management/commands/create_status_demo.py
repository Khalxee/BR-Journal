from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.journal.models import Department, WeeklyJournal
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create sample journal entries with various status tracking'

    def handle(self, *args, **options):
        # Get or create sample users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin / admin123'))

        john, created = User.objects.get_or_create(
            username='john_doe',
            defaults={'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'}
        )
        if created:
            john.set_password('password123')
            john.save()

        jane, created = User.objects.get_or_create(
            username='jane_smith',
            defaults={'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'}
        )
        if created:
            jane.set_password('password123')
            jane.save()

        # Create sample departments
        engineering, _ = Department.objects.get_or_create(
            name='Engineering',
            defaults={'description': 'Software Development Team'}
        )
        
        marketing, _ = Department.objects.get_or_create(
            name='Marketing',
            defaults={'description': 'Marketing and Communications'}
        )

        # Create sample journal entries with different statuses
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        # John's Engineering Entry - Mix of statuses
        john_entry, created = WeeklyJournal.objects.get_or_create(
            author=john,
            department=engineering,
            date_from=week_start,
            date_to=week_end,
            defaults={
                'highlights': [
                    {"text": "Successfully deployed user authentication system to production", "status": "completed"},
                    {"text": "Fixed critical bug in payment processing module", "status": "completed"},
                    {"text": "Completed code review for 5 pull requests", "status": "completed"}
                ],
                'pendings': [
                    {"text": "Database optimization project - 70% complete", "status": "in_progress"},
                    {"text": "Integration with third-party API - waiting for documentation", "status": "on_hold"},
                    {"text": "Performance testing of new features", "status": "not_started"}
                ],
                'challenges': [
                    {"text": "Server memory issues causing intermittent outages", "status": "in_progress"},
                    {"text": "Complex migration script needs more testing", "status": "on_hold"}
                ],
                'personal_updates': [
                    {"text": "Completed Django advanced course certification", "status": "completed"},
                    {"text": "Started learning React for frontend projects", "status": "in_progress"}
                ],
                'strategies': [
                    {"text": "Plan architecture for new microservices", "status": "not_started"},
                    {"text": "Research containerization options for deployment", "status": "not_started"}
                ]
            }
        )

        # Jane's Marketing Entry - Different status mix
        jane_entry, created = WeeklyJournal.objects.get_or_create(
            author=jane,
            department=marketing,
            date_from=week_start,
            date_to=week_end,
            defaults={
                'highlights': [
                    {"text": "Launched Q4 marketing campaign across social media", "status": "completed"},
                    {"text": "Increased email open rates by 25%", "status": "completed"}
                ],
                'pendings': [
                    {"text": "Finalizing content for product launch event", "status": "in_progress"},
                    {"text": "Reviewing vendor proposals for print materials", "status": "in_progress"},
                    {"text": "Budget approval pending for Google Ads campaign", "status": "on_hold"}
                ],
                'challenges': [
                    {"text": "Brand messaging consistency across different channels", "status": "in_progress"},
                    {"text": "Limited budget for video production", "status": "on_hold"},
                    {"text": "Competitor launched similar campaign - need differentiation", "status": "cancelled"}
                ],
                'personal_updates': [
                    {"text": "Attended digital marketing conference", "status": "completed"},
                    {"text": "Working on Google Analytics certification", "status": "in_progress"}
                ],
                'strategies': [
                    {"text": "Develop influencer partnership program", "status": "not_started"},
                    {"text": "Create customer testimonial video series", "status": "not_started"}
                ]
            }
        )

        # Previous week entry for John to show progression
        prev_week_start = week_start - timedelta(days=7)
        prev_week_end = prev_week_start + timedelta(days=6)

        john_prev_entry, created = WeeklyJournal.objects.get_or_create(
            author=john,
            department=engineering,
            date_from=prev_week_start,
            date_to=prev_week_end,
            defaults={
                'highlights': [
                    {"text": "Completed initial setup of CI/CD pipeline", "status": "completed"},
                    {"text": "Resolved 15 bugs from user feedback", "status": "completed"}
                ],
                'pendings': [
                    {"text": "User authentication system development", "status": "completed"},  # This became a highlight this week
                    {"text": "Database optimization research", "status": "in_progress"}  # Still ongoing
                ],
                'challenges': [
                    {"text": "Learning new testing framework", "status": "completed"},
                    {"text": "Server configuration issues", "status": "in_progress"}
                ],
                'personal_updates': [
                    {"text": "Started advanced Django course", "status": "completed"}
                ],
                'strategies': [
                    {"text": "Plan next quarter development roadmap", "status": "completed"}
                ]
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully created sample journal entries with status tracking!'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Sample users created:'))
        self.stdout.write(self.style.SUCCESS('  - admin / admin123 (superuser)'))
        self.stdout.write(self.style.SUCCESS('  - john_doe / password123'))
        self.stdout.write(self.style.SUCCESS('  - jane_smith / password123'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Status types demonstrated:'))
        self.stdout.write(self.style.SUCCESS('  🟢 Completed - Finished tasks and achievements'))
        self.stdout.write(self.style.SUCCESS('  🔵 In Progress - Currently being worked on'))
        self.stdout.write(self.style.SUCCESS('  🟡 On Hold - Temporarily paused'))
        self.stdout.write(self.style.SUCCESS('  ⚪ Not Started - Planned but not yet begun'))
        self.stdout.write(self.style.SUCCESS('  🔴 Cancelled - No longer pursuing'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Run: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('Then visit: http://127.0.0.1:8000/'))

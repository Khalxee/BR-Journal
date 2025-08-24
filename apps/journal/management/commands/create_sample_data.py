from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.journal.models import Department, WeeklyJournal
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Create sample data for BR Journal application with JSON structure'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data for BR Journal...'))

        # Create sample departments
        departments_data = [
            ('Engineering', 'Software Development and Technical Team'),
            ('Marketing', 'Marketing and Communications Team'),
            ('Sales', 'Sales and Business Development Team'),
            ('HR', 'Human Resources Team'),
            ('Finance', 'Finance and Accounting Team'),
            ('Operations', 'Operations and Support Team'),
        ]

        departments = []
        for name, desc in departments_data:
            dept, created = Department.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'Created department: {name}')

        # Create sample users if they don't exist
        users_data = [
            ('john_doe', 'john@example.com', 'John', 'Doe'),
            ('jane_smith', 'jane@example.com', 'Jane', 'Smith'),
            ('mike_wilson', 'mike@example.com', 'Mike', 'Wilson'),
            ('sarah_davis', 'sarah@example.com', 'Sarah', 'Davis'),
        ]

        users = []
        for username, email, first_name, last_name in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            if created:
                user.set_password('password123')  # Set a default password
                user.save()
                self.stdout.write(f'Created user: {username}')
            users.append(user)

        # Create sample journal entries with JSON structure
        today = date.today()
        
        sample_entries = [
            {
                'author': users[0],  # John Doe
                'department': departments[0],  # Engineering
                'date_from': today - timedelta(days=14),
                'date_to': today - timedelta(days=8),
                'highlights': [
                    'Successfully implemented user authentication system',
                    'Completed code review for the payment module',
                    'Fixed critical bug in the checkout process',
                    'Deployed new API version to production'
                ],
                'pendings': [
                    'Waiting for design approval on the new dashboard layout',
                    'Need to complete unit tests for the API endpoints',
                    'Code documentation for the new features'
                ],
                'challenges': [
                    'Encountered integration issues with third-party payment gateway',
                    'Database performance issues during peak hours',
                    'Time zone handling complications'
                ],
                'personal_updates': [
                    'Completed Django REST framework course',
                    'Started learning React for frontend development'
                ],
                'strategies': [
                    'Plan to implement caching for better performance',
                    'Schedule meeting with DevOps team for deployment optimization',
                    'Research better testing frameworks'
                ],
            },
            {
                'author': users[1],  # Jane Smith
                'department': departments[1],  # Marketing
                'date_from': today - timedelta(days=14),
                'date_to': today - timedelta(days=8),
                'highlights': [
                    'Launched successful social media campaign that increased engagement by 40%',
                    'Completed Q3 marketing report with positive results',
                    'Secured partnership with 3 new influencers'
                ],
                'pendings': [
                    'Finalizing content for upcoming product launch',
                    'Waiting for budget approval for paid advertising campaigns'
                ],
                'challenges': [
                    'Low conversion rates on latest email campaign',
                    'Difficulty in reaching target demographic through current channels'
                ],
                'personal_updates': [
                    'Attended digital marketing conference',
                    'Obtained Google Analytics certification'
                ],
                'strategies': [
                    'Test A/B variations for email templates',
                    'Explore partnerships with industry influencers',
                    'Implement retargeting campaigns'
                ],
            },
            {
                'author': users[2],  # Mike Wilson
                'department': departments[2],  # Sales
                'date_from': today - timedelta(days=7),
                'date_to': today - timedelta(days=1),
                'highlights': [
                    'Closed three major deals worth $150K total',
                    'Successfully onboarded two new enterprise clients',
                    'Exceeded monthly quota by 120%'
                ],
                'pendings': [
                    'Following up on pending proposals worth $200K',
                    'Scheduling product demos for potential clients',
                    'Contract negotiations with Fortune 500 company'
                ],
                'challenges': [
                    'Increased competition in the enterprise market',
                    'Longer sales cycles affecting quarterly targets'
                ],
                'personal_updates': [
                    'Completed advanced sales training program',
                    'Networking at industry trade show next week'
                ],
                'strategies': [
                    'Focus on relationship building with existing clients for upselling',
                    'Develop competitive analysis report',
                    'Create case studies from recent successful deals'
                ],
            }
        ]

        for entry_data in sample_entries:
            journal, created = WeeklyJournal.objects.get_or_create(
                author=entry_data['author'],
                date_from=entry_data['date_from'],
                date_to=entry_data['date_to'],
                defaults=entry_data
            )
            if created:
                self.stdout.write(f'Created journal entry for {entry_data["author"].username}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data with JSON structure!')
        )
        self.stdout.write(
            self.style.WARNING('Default user password is "password123" - remember to change this in production!')
        )

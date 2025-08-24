from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.journal.models import Department, WeeklyJournal
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Create additional sample entries for summary report demonstration'

    def handle(self, *args, **options):
        # Ensure we have users and departments
        users = list(User.objects.all())
        departments = list(Department.objects.all())
        
        if not users or not departments:
            self.stdout.write(self.style.ERROR('Please run create_status_demo first to create users and departments.'))
            return
        
        # Create entries for different time periods
        today = date.today()
        
        # Create entries for the past 4 weeks
        entries_created = 0
        for week in range(4):
            week_start = today - timedelta(days=today.weekday() + (week * 7))
            week_end = week_start + timedelta(days=6)
            
            # Create 2-3 entries per week from different users/departments
            for i in range(random.randint(2, 4)):
                user = random.choice(users)
                department = random.choice(departments)
                
                # Skip if entry already exists for this user/week combination
                if WeeklyJournal.objects.filter(
                    author=user, 
                    date_from=week_start, 
                    date_to=week_end
                ).exists():
                    continue
                
                # Try different user/department combinations to avoid conflicts
                attempts = 0
                while attempts < 10:
                    user = random.choice(users)
                    department = random.choice(departments)
                    
                    if not WeeklyJournal.objects.filter(
                        author=user, 
                        date_from=week_start, 
                        date_to=week_end
                    ).exists():
                        break
                    attempts += 1
                
                # Skip this iteration if we couldn't find a unique combination
                if attempts >= 10:
                    continue
                
                # Sample content based on department
                if department.name == 'Engineering':
                    highlights = [
                        {"text": f"Completed bug fixes for user authentication system - Week {week+1}", "status": "completed"},
                        {"text": f"Deployed new API endpoints for mobile app integration", "status": "completed"},
                        {"text": f"Performance optimization reduced page load time by 40%", "status": "completed"}
                    ]
                    challenges = [
                        {"text": f"Database migration taking longer than expected", "status": "in_progress"},
                        {"text": f"Third-party API rate limits causing delays", "status": "on_hold"}
                    ]
                    strategies = [
                        {"text": f"Plan microservices architecture for Q{((today.month-1)//3)+1+1}", "status": "not_started"},
                        {"text": f"Research new testing framework options", "status": "not_started"}
                    ]
                    pendings = [
                        {"text": f"Code review for payment processing module", "status": "in_progress"},
                        {"text": f"Unit tests for new authentication features", "status": "in_progress"}
                    ]
                    personal = [
                        {"text": f"Completed AWS certification course", "status": "completed"},
                        {"text": f"Attending React conference next month", "status": "not_started"}
                    ]
                
                elif department.name == 'Marketing':
                    highlights = [
                        {"text": f"Q{((today.month-1)//3)+1} campaign exceeded targets by 15% - Week {week+1}", "status": "completed"},
                        {"text": f"Social media engagement increased 25%", "status": "completed"},
                        {"text": f"Successfully launched product demo videos", "status": "completed"}
                    ]
                    challenges = [
                        {"text": f"Budget constraints for paid advertising", "status": "on_hold"},
                        {"text": f"Content approval process needs streamlining", "status": "in_progress"}
                    ]
                    strategies = [
                        {"text": f"Develop influencer partnership program", "status": "not_started"},
                        {"text": f"Create automated email nurture sequences", "status": "in_progress"}
                    ]
                    pendings = [
                        {"text": f"Brand guidelines revision in progress", "status": "in_progress"},
                        {"text": f"Website redesign mockups under review", "status": "in_progress"}
                    ]
                    personal = [
                        {"text": f"Completed Google Analytics certification", "status": "completed"},
                        {"text": f"Presenting at marketing summit next quarter", "status": "not_started"}
                    ]
                
                elif department.name == 'Sales':
                    highlights = [
                        {"text": f"Closed 3 major enterprise deals this week - Week {week+1}", "status": "completed"},
                        {"text": f"Pipeline value increased by $50K", "status": "completed"},
                        {"text": f"Customer satisfaction score: 4.8/5", "status": "completed"}
                    ]
                    challenges = [
                        {"text": f"Long sales cycles with enterprise clients", "status": "in_progress"},
                        {"text": f"Competitive pressure in mid-market segment", "status": "on_hold"}
                    ]
                    strategies = [
                        {"text": f"Implement new CRM workflow automation", "status": "not_started"},
                        {"text": f"Develop vertical-specific sales materials", "status": "in_progress"}
                    ]
                    pendings = [
                        {"text": f"Proposal review for Fortune 500 prospect", "status": "in_progress"},
                        {"text": f"Follow-up calls with Q{((today.month-1)//3)+1} prospects", "status": "in_progress"}
                    ]
                    personal = [
                        {"text": f"Attended sales methodology training", "status": "completed"},
                        {"text": f"Working on industry certification", "status": "in_progress"}
                    ]
                
                else:  # Generic for other departments
                    highlights = [
                        {"text": f"Achieved key milestone for department project - Week {week+1}", "status": "completed"},
                        {"text": f"Team collaboration improved significantly", "status": "completed"}
                    ]
                    challenges = [
                        {"text": f"Resource allocation needs optimization", "status": "in_progress"},
                        {"text": f"Process improvements needed", "status": "on_hold"}
                    ]
                    strategies = [
                        {"text": f"Plan process automation initiatives", "status": "not_started"}
                    ]
                    pendings = [
                        {"text": f"Department quarterly planning in progress", "status": "in_progress"}
                    ]
                    personal = [
                        {"text": f"Professional development training completed", "status": "completed"}
                    ]
                
                # Create the journal entry
                entry = WeeklyJournal.objects.create(
                    author=user,
                    department=department,
                    date_from=week_start,
                    date_to=week_end,
                    highlights=highlights,
                    challenges=challenges,
                    strategies=strategies,
                    pendings=pendings,
                    personal_updates=personal
                )
                entries_created += 1
        
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('=== Summary Report Demo Data Created! ==='))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS(f'Created {entries_created} additional journal entries'))
        self.stdout.write(self.style.SUCCESS('Entries span the past 4 weeks across all departments'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('📊 Summary Report Features Available:'))
        self.stdout.write(self.style.SUCCESS('   📅 Date Range Filtering - Filter entries by specific date ranges'))
        self.stdout.write(self.style.SUCCESS('   🏢 Department Filtering - View entries by specific departments'))
        self.stdout.write(self.style.SUCCESS('   👤 Author Filtering - See entries from specific team members'))
        self.stdout.write(self.style.SUCCESS('   🔍 Content Search - Search across all journal entry content'))
        self.stdout.write(self.style.SUCCESS('   📋 Multiple Grouping - Group by date, department, or author'))
        self.stdout.write(self.style.SUCCESS('   📈 Status Analytics - Complete status distribution across all entries'))
        self.stdout.write(self.style.SUCCESS('   🖨️  Print Export - Print-friendly and CSV export options'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Access Summary Report:'))
        self.stdout.write(self.style.SUCCESS('  1. Run: python3 manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('  2. Visit: http://127.0.0.1:8000/'))
        self.stdout.write(self.style.SUCCESS('  3. Navigate: "Summary Report" in the sidebar'))
        self.stdout.write(self.style.SUCCESS('  4. Test: Try different filters and grouping options'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('🎯 Try These Features:'))
        self.stdout.write(self.style.SUCCESS('   • Filter by current month to see recent activity'))
        self.stdout.write(self.style.SUCCESS('   • Group by Department to see team activities'))
        self.stdout.write(self.style.SUCCESS('   • Group by Author to see individual contributions'))
        self.stdout.write(self.style.SUCCESS('   • Search for specific keywords like "authentication" or "campaign"'))
        self.stdout.write(self.style.SUCCESS('   • Export to CSV or print-friendly format'))

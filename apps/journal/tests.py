from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Department, WeeklyJournal


class JournalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.department = Department.objects.create(
            name='Test Department',
            description='Test department description'
        )

    def test_department_creation(self):
        self.assertEqual(self.department.name, 'Test Department')
        self.assertEqual(str(self.department), 'Test Department')

    def test_journal_creation(self):
        journal = WeeklyJournal.objects.create(
            author=self.user,
            department=self.department,
            date_from='2024-01-01',
            date_to='2024-01-07',
            highlights='Test highlights'
        )
        self.assertEqual(journal.author, self.user)
        self.assertEqual(journal.department, self.department)
        self.assertTrue(journal.highlights, 'Test highlights')


class JournalViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.department = Department.objects.create(
            name='Test Department'
        )

    def test_dashboard_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('journal:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_journal_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('journal:list'))
        self.assertEqual(response.status_code, 200)

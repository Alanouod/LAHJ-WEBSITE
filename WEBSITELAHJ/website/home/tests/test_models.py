from django.test import TestCase
from django.contrib.auth.models import User
from home.models import *
from django.db import connection

class ModelTestCase(TestCase):
    def setUp(self):
        # Create test users with unique emails
        self.user1 = User.objects.create_user(username='username1', email='email1@gmail.com', password='password1')
        self.user2 = User.objects.create_user(username='username2', email='email2@gmail.com', password='password2')

        # Create test user profiles with corresponding users
        self.profile1 = UserProfile.objects.create(user=self.user1, phone='123456789', address='Address 1', password=('password123'))
        self.profile2 = UserProfile.objects.create(user=self.user2, phone='987654321', address='Address 2',password=('password123'))

        # Create test homeowners with corresponding users
        self.homeowner1 = Homeowner.objects.create(user=self.user1, phone='123456789', address='Address 1')
        self.homeowner2 = Homeowner.objects.create(user=self.user2, phone='987654321', address='Address 2')

        # Create test professionals with corresponding users
        self.professional1 = Professional.objects.create(user=self.user1, phone='123456789', address='Address 1', bio='Bio 1', job='Job 1')
        self.professional2 = Professional.objects.create(user=self.user2, phone='987654321', address='Address 2', bio='Bio 2', job='Job 2')

    def tearDown(self):
        # Clean up any test data if needed
        pass

    def test_user_profile_creation(self):
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertEqual(UserProfile.objects.get(user=self.user1).user.username, 'username1')
        self.assertEqual(UserProfile.objects.get(user=self.user2).user.username, 'username2')

    def test_homeowner_creation(self):
        self.assertEqual(Homeowner.objects.count(), 2)

    def test_professional_creation(self):
        self.assertEqual(Professional.objects.count(), 2)


class ModelTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        # Close any remaining database connections at the class level
        connection.close()
        super().tearDownClass()

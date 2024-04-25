from django.test import TestCase
from django.urls import reverse
from home.views import *
from django.db import connection  

class TestViews(TestCase):

    def tearDown(self):
        # Close database connections after each test
        connection.close()

    def test_home_view(self):
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

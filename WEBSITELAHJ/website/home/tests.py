from django.test import TestCase
from django.urls import reverse

class HomeViewTestCase(TestCase):
    def test_home_view_status_code(self):
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

from django.test import TestCase
from home.forms import CommentForm
from django.db import connection

class TestForms(TestCase):

    def tearDown(self):
        # Close any lingering database connections
        connection.close()

    def test_comment_form_valid_data(self):
        form = CommentForm(data={'content': 'Great work!'})
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())

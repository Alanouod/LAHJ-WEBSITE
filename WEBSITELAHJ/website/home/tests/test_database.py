from django.test import TestCase, override_settings
from django.db import connection
from django.db.utils import OperationalError
from django.db import DEFAULT_DB_ALIAS
from contextlib import closing

class TestDatabase(TestCase):

    @override_settings(DATABASES={DEFAULT_DB_ALIAS: {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
    def test_destroy_test_database(self):
        # Attempt to destroy the test database
        try:
            with closing(connection.cursor()) as cursor:
                cursor.execute("DROP DATABASE %s;" % connection.creation.test_database_name)
        except OperationalError:
            # Handle the exception if the database cannot be dropped
            pass

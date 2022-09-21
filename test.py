import unittest
import sqlite3
import os

from url import *

class TestShortener(unittest.TestCase):
    def setUp(self):
        self.connection_object = sqlite3.connect("test-testing.db")
        cursor_object = self.connection_object.cursor()
        cursor_object.execute('''
            CREATE TABLE IF NOT EXISTS urls
            (
                short_url TEXT PRIMARY KEY NOT NULL,
                long_url TEXT NOT NULL
            );
            ''')
        cursor_object.execute('''
            CREATE UNIQUE INDEX idx_long_url ON urls (long_url);
            ''')
        self.connection_object.commit()

    def test_url(self):
        longURL = 'https://www.verylongurl.com/big/path/too'
        shortURL = create_shortened_url(longURL, 'test-testing.db')
        self.assertIn("https://www.shorty.com/", shortURL)

        self.assertEqual(get_original_url(shortURL, 'test-testing.db'), longURL)

        with self.assertRaises(sqlite3.Error): create_shortened_url(longURL, 'test-testing.db')

    def tearDown(self):
        if self.connection_object:
            self.connection_object.close()
        os.remove("test-testing.db")

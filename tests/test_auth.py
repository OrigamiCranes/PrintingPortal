from tests.test_base import TestBase
from flask import url_for

class TestRoutes(TestBase):
    def test_access_login(self):
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_access_register(self):
        response = self.client.get(url_for('auth.register'))
        self.assertEqual(response.status_code, 200)

    def test_access_logout(self):
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
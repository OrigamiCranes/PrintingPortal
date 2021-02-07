from app.tests.test_base import TestBase
from flask import url_for
from flask_login import current_user

class TestAccess(TestBase):
    def test_access_index(self):
        response = self.client.get(url_for('printing.index'))
        self.assertEqual(response.status_code, 200)

    def test_access_index_row(self):
        response = self.client.post(url_for('printing.index', row_id=1), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_add(self):
        response = self.client.post(url_for('printing.add'), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_delete(self):
        response = self.client.post(url_for('printing.delete', row_id=1), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_edit(self):
        response = self.client.post(url_for('printing.edit', row_id=1), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_clear(self):
        response = self.client.post(url_for('printing.clear'), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_checkout(self):
        response = self.client.post(url_for('printing.checkout'), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_orderHistory(self):
        response = self.client.post(url_for('printing.orderHistory'), follow_redirects=True)
        self.assertIn(b'Print Order History', response.data)

class TestForms(TestBase):
    def test_form_add(self):
        pass

    def test_form_edit(self):
        pass

    def test_form_filter(self):
        pass